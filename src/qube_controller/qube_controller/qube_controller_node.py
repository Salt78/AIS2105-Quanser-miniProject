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
        self.integrap = min(-5, max(self.integral, 5)) #Windup limit


        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        
        #Resolves deadband issue when regulator output value is small
        if output > 3.0 and output < 10.0:
            output = 10.0
        
        if output > -10.0 and output < -3.0:
            output = -10.0

        clamped = max(-999.0, min(output, 999.0)) #Prevents eratic behaviour from Qube

        self.prev_error = error
        self.prev_time = current_time
        return clamped

class QubeControllerNode(Node):
    def __init__(self):
        super().__init__('qube_controller_node')

        self.declare_parameter('kp', 13.0)
        self.kp = self.get_parameter('kp').get_parameter_value().double_value

        self.declare_parameter('ki', 0.0)
        self.ki = self.get_parameter('ki').get_parameter_value().double_value

        self.declare_parameter('kd', 3.0)
        self.kd = self.get_parameter('kd').get_parameter_value().double_value

        self.declare_parameter('target_position', 0.0)
        self.target_position = self.get_parameter('target_position').get_parameter_value().double_value

        self.add_on_set_parameters_callback(self.parameter_callback)

        self.pid = PID(self.kp, self.ki, self.kd)

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

    
    def joint_state_callback(self, msg: JointState):
        self.latest_joint_state = msg
        self.get_logger().debug(
            f"joint_states received position={msg.position} velocity={msg.velocity}"
        )

        if len(msg.position) > 0:
            current_position = msg.position[0]  
            current_velocity = msg.velocity[0] 
            error = self.target_position - current_position

            current_time = self.get_clock().now()
            control_signal = self.pid.update(error, current_time)

    

            velocity_msg = Float64MultiArray()
            velocity_msg.data = [control_signal]  
            self.velocity_pub.publish(velocity_msg)

            self.get_logger().info(
                f"Error: {error:.3f}, Control: {control_signal:.3f}, Rotor Position: {current_position:.3f}, Rotor Velocity: {current_velocity:.3f}"
            )

    def parameter_callback(self, params):
        """Callback to handle parameter updates."""
        for param in params:
            if param.name == 'target_position':
                if (param.value >= 0.0):
                    self.target_position = param.value
                    self.get_logger().info(f' target was set: {self.target_position}')

                    return SetParametersResult(successful = True)
                return SetParametersResult(successful = False)
            
            if param.name == 'kp':
                if (param.value >= 0.0):
                    self.pid.kp = param.value
                    self.get_logger().info(f' reference was set: {self.pid.kp}')

                    return SetParametersResult(successful = True)
                return SetParametersResult(successful = False)
            
            if param.name == 'ki':
                if (param.value >= 0.0):
                    self.pid.ki = param.value
                    self.get_logger().info(f' reference was set: {self.pid.ki}')

                    return SetParametersResult(successful = True)
                return SetParametersResult(successful = False)
            
            if param.name == 'kd':
                if (param.value >= 0.0):
                    self.pid.kd = param.value
                    self.get_logger().info(f' reference was set: {self.pid.kd}')

                    return SetParametersResult(successful = True)
                return SetParametersResult(successful = False)
    

def main():
    rclpy.init()
    qube_controller_node = QubeControllerNode()
    rclpy.spin(qube_controller_node)

if __name__ == '__main__':
     main()