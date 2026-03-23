import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState 
from rcl_interfaces.msg import SetParametersResult
import numpy as np



class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = None

    def update(self, error, current_time):
        if self.prev_time is None:
            dt = 0.01 
        else:
            dt = (current_time - self.prev_time).nanoseconds / 1e9
            if dt <= 0:
                dt = 0.001 

        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        self.prev_time = current_time
        return output

class QubeControllerNode(Node):
    def __init__(self):
        super().__init__('qube_controller_node')

        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.0)
        self.declare_parameter('kd', 0.1)
        self.declare_parameter('target_position', 0.0)

        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        self.pid = PID(kp, ki, kd)

        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.velocity_pub = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10
        )

        self.latest_joint_state = None
        self.target_position = self.get_parameter('target_position').value

    
    def joint_state_callback(self, msg: JointState):
        self.latest_joint_state = msg
        self.get_logger().debug(
            f"joint_states received position={msg.position} velocity={msg.velocity} effort={msg.effort}"
        )

        if len(msg.position) > 0:
            current_position = msg.position[0]  
            current_velocity = msg.velocity[0] if len(msg.velocity) > 0 else 0.0
            error = self.target_position - current_position

            current_time = self.get_clock().now()
            control_signal = self.pid.update(error, current_time)

            # Publish as Float64MultiArray
            velocity_msg = Float64MultiArray()
            velocity_msg.data = [control_signal]  
            self.velocity_pub.publish(velocity_msg)

            self.get_logger().info(
                f"Error: {error:.3f}, Control: {control_signal:.3f}, Rotor Position: {current_position:.3f}, Rotor Velocity: {current_velocity:.3f}"
            )
    

def main():
    rclpy.init()
    qube_controller_node = QubeControllerNode()
    rclpy.spin(qube_controller_node)

if __name__ == '__main__':
     main()