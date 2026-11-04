Adaptive Embedded Control and Sensor Fusion for Intelligent Autonomous Mobile Robots

A mobile robot simulation developed using ROS 2 Humble and Gazebo Classic. The project focuses on obstacle detection, robot movement, sensor integration and localization in an environment containing multiple obstacles.

About the Project

The main objective of this project is to study how a mobile robot can navigate an environment while detecting obstacles and monitoring its own movement.

A differential-drive robot is modelled in Gazebo with a simulated 360-degree LiDAR and IMU. ROS 2 handles communication between the different components. LiDAR data is used by the obstacle avoidance node to detect nearby objects and decide how the robot should move.

Wheel odometry and IMU measurements are also considered for localization. An Extended Kalman Filter (EKF) configuration is included to combine these sensor inputs. Simulation data is recorded in CSV format and used for further analysis in MATLAB.

The work brings together robot modelling, sensor-based control, ROS 2 communication and performance analysis in one simulation environment.

How the System Works

The robot is controlled through ROS 2 nodes, while Gazebo provides the simulated environment and sensor measurements.

The LiDAR publishes distance measurements through the /scan topic. The obstacle avoidance node processes these measurements and publishes velocity commands through /cmd_vel. Gazebo's differential-drive plugin uses these commands to move the robot.

The robot's movement is also represented through odometry on /odom. The simulated IMU provides orientation-related measurements through /imu/data. The project includes an EKF configuration for combining odometry and IMU data using the robot_localization package.

Simulation measurements are recorded for analysis. The resulting data is used to study the robot's trajectory, linear and angular velocities, obstacle distances and localization performance.

Tools and Technologies

Technology

Application

ROS 2 Humble

Communication between robot components

Gazebo Classic 11

Robot and environment simulation

Python

Control and data logging nodes

URDF

Robot model description

LiDAR

Obstacle detection and distance measurement

IMU

Orientation measurements

robot_localization

EKF configuration for sensor fusion

MATLAB

Analysis and visualization of simulation data

Repository Structure

adaptive-mobile-robot/
│
├── lesson01_webcam/
│
├── obstacle_model/
│   └── obstacle.sdf
│
├── ros2_ws/
│   ├── src/
│   │   └── sentry_camera/
│   │       ├── config/
│   │       │   └── ekf.yaml
│   │       ├── models/
│   │       │   └── mobile_robot.urdf
│   │       ├── sentry_camera/
│   │       │   ├── obstacle_avoidance.py
│   │       │   ├── target_controller.py
│   │       │   ├── data_logger.py
│   │       │   ├── comparison_logger.py
│   │       │   ├── camera_publisher.py
│   │       │   └── camera_subscriber.py
│   │       ├── package.xml
│   │       └── setup.py
│   │
│   ├── worlds/
│   │   └── smart_bot.world
│   │
│   └── results/
│       ├── plots/
│       ├── simulation_log.csv
│       ├── comparison_log.csv
│       └── analyze_smart_bot.m
│
└── README.md

Running the Project

The simulation environment is intended for Ubuntu 22.04 with ROS 2 Humble and Gazebo Classic 11.

Prerequisites

Ubuntu 22.04 LTS, ROS 2 Humble, Gazebo Classic 11, Python 3 and the required ROS 2 packages are needed. MATLAB is optional and is used for analysing the recorded results.

1. Clone the repository

git clone https://github.com/challabhavithsai0123-cell/adaptive-mobile-robot.git

2. Open the ROS 2 workspace

cd adaptive-mobile-robot/ros2_ws

3. Source ROS 2

source /opt/ros/humble/setup.bash

4. Install package dependencies

rosdep install --from-paths src --ignore-src -r -y

5. Build the workspace

colcon build --symlink-install

6. Source the workspace

source install/setup.bash

7. Start the simulation

Start Gazebo Classic with ROS integration, load the worlds/smart_bot.world environment and spawn the robot using the model at:

src/sentry_camera/models/mobile_robot.urdf

Once the robot and its LiDAR topic are available, run the obstacle avoidance node:

ros2 run sentry_camera obstacle_avoidance

The package also provides the following executables:

ros2 run sentry_camera data_logger
ros2 run sentry_camera target_controller

The EKF configuration is located at src/sentry_camera/config/ekf.yaml. To run sensor fusion, the robot_localization package must be installed and the EKF node must be started with this configuration.

Simulation Results

The simulation generates data that can be used to examine the robot's movement and response to its surroundings.

Robot trajectory



Linear velocity



Angular velocity



LiDAR obstacle distance



Additional plots and recorded data are available in the ros2_ws/results/ directory.

MATLAB Analysis

The project includes a MATLAB script named analyze_smart_bot.m, located in ros2_ws/results/.

It is used to analyse recorded simulation data and compare robot movement and localization measurements. The analysis includes trajectory comparison, localization error, linear velocity, angular velocity and nearest obstacle distance.

These results help evaluate the behaviour of the simulated robot rather than relying only on its movement in the Gazebo window.

Scope of the Project

This project is currently a software-based simulation. The robot, LiDAR and IMU are modelled in Gazebo; a physical STM32 board and real sensors are not part of the implemented simulation.

The project provides a basis for extending the control architecture to embedded hardware. Future work could include STM32 integration, hardware-in-the-loop testing, real sensor interfacing, more advanced path planning and wireless telemetry.

Author

Bhavith Sai

B.Tech Student | Robotics and Embedded Systems

GitHub: https://github.com/challabhavithsai0123-cell

This repository contains the ROS 2 package, robot model, simulation world, recorded results and MATLAB analysis files.