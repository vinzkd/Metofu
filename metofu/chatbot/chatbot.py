#!/usr/bin/env python3

# ROS libraries
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Chatbot libraries
import os
from openai import OpenAI
from datetime import datetime
import re

# Python libraries
import serial
from threading import Thread
from time import sleep
from subprocess import run

# Names/Variables
arduinoPath = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)  # Path to arduino
llmModel = "openai/gpt-oss-120b:free"       # Name of LLM model to use for chatbot


# class metofu_controller(Node):
#     def __init__(self):
#         super().__init__("metofu_controller")
#
#         self.Twist_subscription = self.create_subscription(
#                 Twist,                  # Message Type to expect
#                 '/cmd_vel',             # Topic name to listen to
#                 self.velocity_callback, # Function to call when message arrives
#                 10                      # QoS depth
#         )
#         self.get_logger().info("Twist Subscriber initialized, waiting for /cmd_vel...")
#         # self.timer = self.create_timer(0.02, self.main_loop)
#
#
#     def velocity_callback(self, msg):
#         msg.angular.z = 0
#         command += "\n"
#         arduino.write(command.encode())
#         self.sleep(0.1)


class Chatbot:
    def __init__(self, env_path=".env", history_path="history.txt"):
        print("Initializing Chatbot")
        self.OpenAI = OpenAI
        self.datetime = datetime
        self.re = re
        with open(env_path, "r") as file:
            api_key = file.read().strip()
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        os.environ["OPENAI_API_KEY"] = api_key  # Insert API_KEY into .env
        self.history_path = history_path
        self.action_handler = ActionHandler(history_path)

    def send_message(self, message, audio=False, arduino=None):
        with open(self.history_path, "r") as file:
            history = file.readlines()
        response_chunks = []
        stream = self.client.chat.completions.create(
            model=llmModel,
            messages=[
                {"role": "system", "content": f'''
                The current time is {self.datetime.now().strftime("%H:%M:%S")}.
                Here is the conversation so far:
                --
                {history}
                --
                Your primary goal is to chat with the user.
                Never use emojis in your responses.
                Keep your responses at a maximum of 4 sentences.
                If you interpret the user to be giving you a command, respond like so:
                ~action~ACTION_NAME The rest of your response here
                For example, the user says "Please clear the chat history" you respond with:
                ~action~clear_history Okay, I have cleared the chat history.
                Currently, the following actions are supported:
                ~action~clear_history
                ~action~move_forward
                ~action~move_backward
                ~action~turn_left
                ~action~turn_right
                ~action~stop_moving
                ~action~shake_head
                ~action~take_picture
                '''},
                {"role": "user", "content": message}
            ],
            temperature=1,
            stream=True,
        )
        print("BMO: ", end="", flush=True)
        for chunk in stream:
            if hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    response_chunks.append(content)
        response = "".join(response_chunks)
        print()  # Newline after streaming
        with open(self.history_path, "a") as file:
            file.write(f"User: {message}\n")
            file.write(f"BMO: {response}\n")
        match = self.re.match(r"(~action~\w+)\s*(.*)", response)
        if match:
            response = [match.group(1), match.group(2)]

            # Send detected command to action_handler  NOTE: Idk what the part after action_response = ... line does. Consider deleting
            
            #action_response = self.action_handler.handle(response[0], message, arduino, self.client)
            #response = action_response or response[1]
            #print(response) if action_response else ""


            #self.action_handler.handle(response[0], message, arduino, self.client)
            actionCommand = match.group(1)

    def startChat(self):
        while True:
            message = input("You: ")
            self.send_message(message, audio=False)



class ActionHandler:
    def __init__(self, history_path="history.txt"):
        self.sleep = sleep
        self.history_path = history_path

    def send_command(self, command, arduino):
        command += "\n"
        arduino.write(command.encode())
        self.sleep(0.1)


    def handle(self, action, message, arduino, client=None):
        action = action.replace("~action~", "")
        match action:
            case "clear_history":
                file = open(self.history_path, "w")
                file.close()
            case "move_forward":
                self.send_command("move_forward", arduino)
            case "move_backward":
                self.send_command("move_backward", arduino)
            case "turn_left":
                self.send_command("turn_left", arduino)
            case "turn_right":
                self.send_command("turn_right", arduino)
            # case "stop_moving":
            #     return self.send_command("stop_moving", arduino)
            case "shake_head":
                self.send_command("shake_head", arduino)
            case _:
                return "I'm sorry, I don't understand that action."


def main(args=None):
    bot = Chatbot()

    bot.startChat()


if __name__ == "__main__":
    main()
