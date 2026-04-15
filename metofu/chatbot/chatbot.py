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
llmModel = "openai/gpt-oss-120b:free"       # Name of LLM model to use for chatbot

class Chatbot:
    def __init__(self):
        print("Initializing Chatbot")
        self.OpenAI = OpenAI
        self.datetime = datetime
        self.re = re
        
        api_key = os.getenv('API_KEY')
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        history_path = "/home/metofu/history.txt"
        self.history_path = history_path

    def send_message(self, message, audio=False):
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

            actionCommand = match.group(1)

            return actionCommand 
        else:
            return 0

    def startChat(self):
        message = input("You: ")
        answer = self.send_message(message, audio=False)
        return answer



# class ActionHandler:
#     def __init__(self, history_path="history.txt"):
#         self.sleep = sleep
#         self.history_path = history_path


def main(args=None):
    bot = Chatbot()

    bot.startChat()


if __name__ == "__main__":
    main()
