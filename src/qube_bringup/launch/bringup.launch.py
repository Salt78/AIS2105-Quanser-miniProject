from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro
import os

xacro_file = os.path.join(get_package_share_directory("qube_bringup"),"urdf","controlled_qube.urdf.xacro")
robot_description_content = xacro.process_file(xacro_file).toxml()

launch_dir = PathJoinSubstitution([FindPackageShare('qube_driver'), 'launch'])

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(get_package_share_directory("qube_bringup"), 'rviz', 'urdf.rviz')]]
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),
         Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        IncludeLaunchDescription(
            PathJoinSubstitution([launch_dir, 'qube_driver.launch.py']),
            launch_arguments={
                'robot_description': robot_description_content
            }.items()
        )       
    ])