# ROS libraries
import rclpy                        # ROS libraries for python
from rclpy.node import Node         # Node class
from geometry_msgs.msg import Twist # Twist message
from sensor_msgs.msg import Joy     # Joy message

# Python libraries
import serial
import time

arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)  # Serial port arduino is connected to

class robot_controller(Node):

    def __init__(self):
        super().__init__("robot_controller")

        # Shared Joystick Input Data
        self.left_joystick_V = 0
        self.right_joystick_H = 0
        self.dpad_H = 0

        self.Twist_subscription = self.create_subscription(
                Twist,                  # Message Type to expect
                '/cmd_vel',             # Topic name to listen to
                self.velocity_callback, # Function to call when message arrives
                10                      # QoS depth
        )
        self.get_logger().info("Twist Subscriber initialized, waiting for /cmd_vel...")

        self.Joy_subscription = self.create_subscription(
                Joy,                    # Expecting Joy message
                '/joy',                 # Listen to /joy topic
                self.joy_callback,      # Execute joy_callback function when message arrives
                10                      # QoS depth
        )
        self.get_logger().info("Joy Subscriber initialized, waiting for /joy...")


        # Start main loop
        self.timer = self.create_timer(0.02, self.main_loop)

    def velocity_callback(self, msg): 

        self.left_joystick_V = msg.linear.x
        self.right_joystick_H = msg.angular.z


    def joy_callback(self, msg):  # Grab output of /joy message

        buttons = msg.buttons
        axes = msg.axes

        ### Axis Index

        # Left/Up +   Right/Down - 

        # 0 - LeftStick Horizontal
        # 1 - LeftStick Vertical
        # 2 - Left Analog Trigger
        # 3 - RightStick Horizontal
        # 4 - RightStick Vertical
        # 5 - Right Analog Trigger
        # 6 - DPad Horizontal
        # 7 - DPad Vertical

        self.dpad_H = axes[6]


    def main_loop(self):
        command_string = f"{self.left_joystick_V:.2f}:{self.right_joystick_H:.2f}:{self.dpad_H}" 
        send_command(command_string)

        self.get_logger().info( command_string )





def send_command(command):
    command += "\n"
    arduino.write(command.encode())
    return command


def main(args=None):
    print(f"Connected to {arduino.name}")

    rclpy.init(args=args)
    node = robot_controller()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
