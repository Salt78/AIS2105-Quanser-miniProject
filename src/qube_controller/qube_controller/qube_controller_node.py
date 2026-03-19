import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rcl_interfaces.msg import SetParametersResult
import numpy as np


class QubeControllerNode(Node):
     def __init__(self):
          super().__init__('qube_controller_node')

    
    

def main():
    rclpy.init()

    qube_controller_node = QubeControllerNode()

    rclpy.spin(qube_controller_node)

if __name__ == '__main__':
     main()