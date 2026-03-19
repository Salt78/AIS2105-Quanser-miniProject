import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState 
from rcl_interfaces.msg import SetParametersResult
import numpy as np


class QubeControllerNode(Node):
    def __init__(self):
        super().__init__('qube_controller_node')

        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.latest_joint_state = None

    
    def joint_state_callback(self, msg: JointState):
        # store or process joint states; head: [q1, q2], vel: [dq1, dq2], effort maybe
        self.latest_joint_state = msg
        self.get_logger().debug(
            f"joint_states received position={msg.position} velocity={msg.velocity} effort={msg.effort}"
        )

    
    

def main():
    rclpy.init()

    qube_controller_node = QubeControllerNode()

    rclpy.spin(qube_controller_node)

if __name__ == '__main__':
     main()