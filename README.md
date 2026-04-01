# AIS2105 - Mini project

This is a ROS2 project with the goal of controlling and visualizing a Quanser cube. A PID controller is used for controlling the cube. Rviz2 is used for for the visualization. It is also possible to run this project without the physical cube hardware (simulation).

## Depedencies
* ros-jazzy-xacro
* ros-jazzy-ros2-control
* ros-jazzy-ros2-controller

## How to build and run?

```
git clone --recurse-submodules https://github.com/Salt78/AIS2105-Quanser-miniProject.git
cd AIS2105-Quanser-miniProject
colcon build
source install/setup.bash

```

The project can be run by using this launch file:

```
ros2 launch qube_bringup bringup.launch.py
```

The launch file supports the following arguments with these default values:
* baud_rate = 115200
* device = /dev/ttyACM0
* simulation = false

Example of simulation enabled:
```
ros2 launch qube_bringup bringup.launch.py simulation:=true
```

The parameters kP, kI, kD and setpoint of the PID controller can be changed by using param set:
### setpoint 
```
ros2 param set /qube_controller_node target_position value
```
### kP
```
ros2 param set /qube_controller_node kp value
```
### kI
```
ros2 param set /qube_controller_node ki value
```
### kD
```
ros2 param set /qube_controller_node kd value
```

## Troubleshooting
After running the launch file you might be stuck on this warning:
```
[spawner_velocity_controller]: Could not contact service /controller_manager/list_controllers
[spawner-4] [INFO] [1775046460.785208051] [spawner_velocity_controller]: waiting for service /controller_manager/list_controllers to become available...
```
This issue can be fixed by replacing the launch file within src/qube_driver/launch/qube_driver.launch.py with /fixed_qube_driver.launch.py.