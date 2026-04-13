# Import Chatbot class
from chatbot import Chatbot

# ROS libraries
import rclpy                        # ROS libraries for python
from rclpy.node import Node         # Node class
from geometry_msgs.msg import Twist # Twist message

# Serial port arduino is connected to
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)  

class metofu_chatbot(Node):
    def __init__(self):
        super().__init__("metofu_chatbot")

        self.Twist_subscription = self.create_subscription(
                Twist,                  # Message Type to expect
                '/cmd_vel',             # Topic name to listen to
                self.velocity_callback, # Function to call when message arrives
                10                      # QoS depth
        )
        self.get_logger().info("Twist Subscriber initialized, waiting for /cmd_vel...")


def main(args=None):
    print(f"Connected to {arduino.name}")

    rclpy.init(args=args)
    node = metofu_chatbot()

    while True:
        message = input("You: ")
        bot.send_message(message, audio=False, arduino=arduino)

if __name__ == '__main__':
    main()


