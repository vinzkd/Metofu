#!/usr/bin/env python


# ROS libraries
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


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

        self.get_logger().info("Twist publisher initialized")


    def velocity_publish(self):

        # Not needed values
        velocity.linear.y = 0.0
        velocity.linear.z = 0.0
        velocity.angular.x = 0.0
        velocity.angular.y = 0.0

        # Values used for car

        velocity.linear.x = 1.0     # Move forward/backward
        velocity.angular.z = 0.5    # Turn left/right (+/-)
 
        self.publisher_.publish(velocity)



def main(args=None):
    rclpy.init(args=args) 
    node = TwistPublisher()
     
    while True:
        rclpy.spin_once(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 

