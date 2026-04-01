from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

xacro_file = os.path.join(get_package_share_directory("qube_bringup"),"urdf","controlled_qube.urdf.xacro")

launch_dir = PathJoinSubstitution([FindPackageShare('qube_driver'), 'launch'])

def launch_setup(context, *args, **kwargs):
    simulation = LaunchConfiguration('simulation').perform(context)
    baud_rate = LaunchConfiguration('baud_rate').perform(context)
    device = LaunchConfiguration('device').perform(context)

    xacro_doc = xacro.process_file(
        xacro_file,
        mappings={
            'simulation': simulation,
            'baud_rate': baud_rate,
            'device': device
        }
    )

    robot_description = {'robot_description': xacro_doc.toxml()}
    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen'
        )
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('baud_rate', default_value='115200'),
        DeclareLaunchArgument('device', default_value='/dev/ttyACM0'),
        DeclareLaunchArgument('simulation', default_value='false'),
        OpaqueFunction(function=launch_setup),
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