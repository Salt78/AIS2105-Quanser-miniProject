from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

xacro_file = os.path.join(get_package_share_directory("qube_bringup"),"urdf","controlled_qube.urdf.xacro")

launch_dir = PathJoinSubstitution([FindPackageShare('qube_driver'), 'launch'])

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('baud_rate', default_value='115200'),
        DeclareLaunchArgument('device', default_value='/dev/ACM0'),
        DeclareLaunchArgument('simulator', default_value='false'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command([ #Processes Xacro while passing launch parameters
                'xacro', ' ',
                xacro_file, ' ',
                'baud_rate:=', LaunchConfiguration('baud_rate'), ' ',
                'device:=', LaunchConfiguration('device'), ' ',
                'simulator:=', LaunchConfiguration('simulator')
            ])}]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(get_package_share_directory("qube_bringup"), 'rviz', 'urdf.rviz')]]
        ),
       # Node(
       #    package='joint_state_publisher_gui',
       #    executable='joint_state_publisher_gui',
       #    name='joint_state_publisher_gui'
       #),
        IncludeLaunchDescription( #Launches launch file for qube_driver
            PathJoinSubstitution([launch_dir, 'qube_driver.launch.py']),
        ),
        Node(
            package='qube_controller',
            name='qube_controller',
            executable='qube_controller_node',
        ),       
    ])