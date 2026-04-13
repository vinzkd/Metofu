#!/usr/bin/env python

# ROS libraries
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import serial

# Serial port arduino is connected to
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)  


class TwistSubscriber(Node):
    def __init__(self):
        super().__init__("TwistSubscriber")

        self.subscriber_ = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.velocity_callback,     # Function to call for every message received
            10
        )

        self.get_logger().info("Twist subscriber initialized")


    def velocity_callback(self, msg):
        
        # Velocity in format of linear.x:angular.z
        command = f"{msg.linear.x}:{msg.angular.z}" 

        self.get_logger().info( f"sent {command}" )

        



def main(args=None):
    print(f"Connected to {arduino.name}")
    rclpy.init(args=args) 
    node = TwistSubscriber()
     
    # spin() simply keeps python from exiting until this node is stopped
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 
