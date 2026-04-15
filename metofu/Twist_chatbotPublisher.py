#!/usr/bin/env python

# ROS libraries
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Chatbot 
from metofu.chatbot.chatbot import Chatbot

# Python
import time


class TwistPublisher(Node):
    def __init__(self):
        super().__init__("TwistPublisher")

        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.velocity = Twist()
        # timer_period = 1.0  # seconds
        # self.timer = self.create_timer(timer_period, self.velocity_publish)

        self.get_logger().info("Twist chatbot publisher initialized")


    def velocity_publish(self, action):

        # Not needed values
        self.velocity.linear.y = 0.0
        self.velocity.linear.z = 0.0
        self.velocity.angular.x = 0.0
        self.velocity.angular.y = 0.0

        linearx = 0
        angularz = 0
        if action == 0:
            self.velocity.linear.x = 0.0 
            self.velocity.angular.z = 0.0
        else:
            action = action.replace("~action~", "")
            match action:
                case "move_forward":
                    self.velocity.linear.x = 1.0  
                    self.publisher_.publish(self.velocity)
                    time.sleep(2)
                    self.velocity.linear.x = 0.0   
                    self.publisher_.publish(self.velocity)

                case "move_backward":
                    self.velocity.linear.x = -1.0   
                    self.publisher_.publish(self.velocity)
                    time.sleep(2)
                    self.velocity.linear.x = 0.0     
                    self.publisher_.publish(self.velocity)

                case "turn_left":
                    self.velocity.angular.z = 1.0   
                    self.publisher_.publish(self.velocity)
                    time.sleep(2)
                    self.velocity.angular.z = 0.0     
                    self.publisher_.publish(self.velocity)

                case "turn_right":
                    self.velocity.angular.z = 1.0   
                    self.publisher_.publish(self.velocity)
                    time.sleep(2)
                    self.velocity.angular.z = 0.0     
                    self.publisher_.publish(self.velocity)
                case _:
                    print("eh?")

 



def main(args=None):
    rclpy.init(args=args) 
    node = TwistPublisher()
    bot = Chatbot()
     
    while True:
        output = bot.startChat() 
        node.velocity_publish(output)
        rclpy.spin_once(node, timeout_sec=0)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 

