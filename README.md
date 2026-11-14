# Adaptive Embedded Control and Sensor Fusion for Intelligent Autonomous Mobile Robots

A ROS 2 Humble and Gazebo Classic simulation project exploring differential-drive motion, reactive LiDAR obstacle avoidance, simulated IMU sensing, planar state estimation and experiment logging.

> **Scope:** This repository is a software simulation. The robot, LiDAR and IMU are simulated in Gazebo; this is separate from the physical STM32 SENTRY robot.

## Architecture

~~~text
Gazebo world + URDF robot
  |-- /scan (360° simulated LiDAR, 10 Hz)
  |-- /imu/data (simulated IMU, 50 Hz)
  |-- /odom (differential-drive odometry)
  |
  v
ROS 2 obstacle_avoidance
  | subscribes /scan
  | publishes /cmd_vel
  v
Gazebo differential-drive plugin --> robot motion

/odom + /imu/data --> robot_localization EKF configuration
                         |
                         +--> /odometry/filtered

Gazebo model state + sensor topics --> CSV loggers --> MATLAB plots
~~~

## Implemented components

| Component | Implementation |
|---|---|
| Robot model | Differential-drive URDF, two driven wheels and caster |
| LiDAR | 360° simulated ray sensor, 360 samples, 10 Hz |
| IMU | Simulated Gazebo IMU, 50 Hz |
| Drive | Gazebo differential-drive plugin; 0.34 m wheel separation, 0.14 m wheel diameter |
| Obstacle avoidance | Reactive ROS 2 node using front/left/right scan sectors |
| State estimation | robot_localization EKF configuration in 2D mode |
| Logging | CSV data logger and Gazebo-ground-truth comparison logger |
| Analysis | MATLAB script and committed plots |

### Obstacle avoidance behaviour

The obstacle_avoidance node subscribes to /scan and publishes Twist commands to /cmd_vel. It checks front (−25° to +25°), left (35° to 100°) and right (−100° to −35°) sectors. The front obstacle trigger is 0.80 m; the clear-path threshold is 1.00 m. It chooses a turn direction using estimated left/right clearance and stops when front scan data is missing or the scan stream times out.

This is reactive obstacle avoidance, not a global path planner or SLAM implementation.

### EKF configuration

The supplied ekf.yaml configures robot_localization in 2D mode at 30 Hz. It uses /odom for selected planar pose and velocity measurements and /imu/data for Z-axis angular velocity. It does not fuse a full 6-axis IMU solution. The EKF node must be launched separately; no EKF launch file is currently provided. The configuration sets publish_tf to false.

### Data logging

- data_logger records elapsed time, odometry position, linear/angular velocity and nearest front-sector LiDAR distance.
- comparison_logger records Gazebo model-state ground truth, /odom, /odometry/filtered, IMU Z angular velocity and nearest valid LiDAR range.
- CSV logs, plots and analyze_smart_bot.m are in ros2_ws/results/.

**Current path limitation:** both logger scripts use ~/sentry_ros_v2/ros2_ws/results as their output directory. Update that path if your workspace is elsewhere.

## Repository layout

~~~text
adaptive-mobile-robot/
├── lesson01_webcam/
├── obstacle_model/
└── ros2_ws/
    ├── src/sentry_camera/
    │   ├── config/ekf.yaml
    │   ├── models/mobile_robot.urdf
    │   └── sentry_camera/
    │       ├── obstacle_avoidance.py
    │       ├── target_controller.py
    │       ├── data_logger.py
    │       ├── comparison_logger.py
    │       └── camera_*.py
    ├── worlds/smart_bot.world
    └── results/
        ├── CSV logs
        ├── PNG plots
        └── analyze_smart_bot.m
~~~

## Requirements

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Gazebo Classic 11
- colcon, rosdep and the package dependencies
- MATLAB (optional, for the analysis script)

Gazebo Classic is a legacy simulator. Use a compatible ROS 2 Humble / Gazebo Classic environment to reproduce the original setup.

## Build

~~~bash
git clone https://github.com/challabhavithsai0123-cell/adaptive-mobile-robot.git
cd adaptive-mobile-robot/ros2_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
~~~

After spawning the robot in Gazebo and confirming /scan is publishing:

~~~bash
ros2 run sentry_camera obstacle_avoidance
ros2 run sentry_camera data_logger
~~~

The comparison logger also requires Gazebo model states and the EKF output topic:

~~~bash
ros2 run sentry_camera comparison_logger
~~~

The target_controller is a separate command-interface node. It listens on /target/direction and publishes text commands on /robot/control_command; it is not connected directly to /cmd_vel in the current code.

~~~bash
ros2 run sentry_camera target_controller
~~~

The EKF configuration is at src/sentry_camera/config/ekf.yaml. Launch robot_localization separately using this file.

## Results

Committed artifacts in ros2_ws/results/ include trajectory, linear/angular velocity, obstacle-distance and localization-error plots, plus CSV logs. The MATLAB script analyze_smart_bot.m supports further analysis.

These artifacts document simulation and analysis. They are not evidence of physical-hardware validation or a controlled benchmark unless the experimental setup and repeatability are established.

## Limitations and next steps

- Replace hard-coded logger paths with configurable ROS parameters.
- Add a launch file for the robot, controllers, loggers and EKF.
- Connect the target-controller command interface to a defined motion-control node.
- Add automated tests for missing scans, invalid ranges, narrow passages and timeout behaviour.
- Validate simulation dynamics before using them to predict real hardware behaviour.
- Treat the older URDF/world backup files as historical copies, not active models.

## Author

**C. Bhavith Sai**  
B.Tech — Mechatronics Engineering  
[GitHub profile](https://github.com/challabhavithsai0123-cell)

**Areas:** ROS 2 · Gazebo Classic · Mobile Robotics · LiDAR · Sensor Fusion · EKF · Python · MATLAB
