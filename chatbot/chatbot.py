# # ROS libraries
# import rclpy                        # ROS libraries for python
# from rclpy.node import Node         # Node class
# from geometry_msgs.msg import Twist # Twist message
# from sensor_msgs.msg import Joy     # Joy message

# Chatbot libraries
from actions import ActionHandler
import os
from openai import OpenAI
from datetime import datetime
import re
import pyaudio

# Python libraries
import serial

# Names/Variables
arduinoPath = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)  # Path to arduino
modelName = "openai/gpt-oss-20b:free"       # Name of LLM model to use for chatbot


class ChatBot:
    def __init__(self, env_path=".env", history_path="history.txt"):
        self.OpenAI = OpenAI
        self.datetime = datetime
        self.re = re
        with open(env_path, "r") as file:
            api_key = file.read().strip()
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        os.environ["OPENAI_API_KEY"] = api_key
        self.history_path = history_path
        self.action_handler = ActionHandler(history_path)

    def send_message(self, message, audio=False, arduino=None):
        with open(self.history_path, "r") as file:
            history = file.readlines()
        response_chunks = []
        stream = self.client.chat.completions.create(
            model=modelName,
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
            action_response = self.action_handler.handle(response[0], message, arduino, self.client)
            response = action_response or response[1]
            print(response) if action_response else ""

if __name__ == "__main__":
    arduino = arduinoPath
    bot = ChatBot()
    print(arduino)
    print(modelName)
    while True:
        message = input("You: ")
        bot.send_message(message, audio=True, arduino=arduino)
