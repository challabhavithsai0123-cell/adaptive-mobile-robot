\# Adaptive Embedded Control and Sensor Fusion for Intelligent Autonomous Mobile Robots



A ROS 2 and Gazebo-based autonomous mobile robot simulation integrating LiDAR-based obstacle avoidance, IMU sensing, wheel odometry, Extended Kalman Filter (EKF) localization, and performance analysis.



\## Project Overview



Autonomous mobile robots must navigate unfamiliar environments while avoiding obstacles and maintaining accurate localization.



This project explores an integrated robotics architecture using ROS 2 Humble and Gazebo Classic. A differential-drive robot is simulated in an environment containing multiple obstacles. LiDAR data is used for reactive obstacle avoidance, while wheel odometry and simulated IMU measurements are configured for sensor fusion using an Extended Kalman Filter.



Simulation data is recorded and analyzed to evaluate robot motion, obstacle distances, and localization performance.



\## Key Features



\- \*\*Differential-Drive Robot:\*\* Simulated two-wheel mobile robot.

\- \*\*360° LiDAR:\*\* Simulated laser scanning for environmental perception.

\- \*\*IMU Integration:\*\* Simulated IMU measurements for orientation sensing.

\- \*\*Obstacle Avoidance:\*\* Reactive obstacle detection and navigation using LiDAR.

\- \*\*Sensor Fusion:\*\* EKF configuration combining wheel odometry and IMU data.

\- \*\*Gazebo Simulation:\*\* Multi-obstacle simulation environment.

\- \*\*Data Logging:\*\* Records simulation measurements into CSV files.

\- \*\*MATLAB Analysis:\*\* Compares ground truth, wheel odometry and EKF localization results.



\## System Architecture



```text

&#x20;            Gazebo Simulation

&#x20;                   |

&#x20;         Differential Drive Robot

&#x20;                   |

&#x20;         +---------+---------+

&#x20;         |                   |

&#x20;      360° LiDAR         Simulated IMU

&#x20;         |                   |

&#x20;      /scan              /imu/data

&#x20;         |                   |

&#x20;         v                   v

&#x20;    Obstacle             Sensor Fusion

&#x20;    Avoidance                |

&#x20;         |                  EKF

&#x20;         |                   |

&#x20;         +--------+----------+

&#x20;                  |

&#x20;             Robot Motion

&#x20;                  |

&#x20;               /odom

&#x20;                  |

&#x20;            Data Logging

&#x20;                  |

&#x20;               CSV Data

&#x20;                  |

&#x20;            MATLAB Analysis

&#x20;                  |

&#x20;         Performance Graphs

```



\## Technologies Used



| Technology | Purpose |

|---|---|

| ROS 2 Humble | Robotics middleware |

| Gazebo Classic 11 | Robot and environment simulation |

| Python | ROS 2 nodes and control logic |

| URDF | Robot description and modeling |

| LiDAR | Obstacle perception |

| IMU | Orientation measurements |

| robot\_localization / EKF | Sensor fusion configuration |

| MATLAB | Data analysis and visualization |

| CSV | Simulation data storage |



\## Project Structure



```text

adaptive-mobile-robot/

│

├── lesson01\_webcam/

│   ├── frame\_inspection.py

│   ├── live\_video.py

│   ├── pixel\_inspection.py

│   └── webcam\_test.py

│

├── obstacle\_model/

│   └── obstacle.sdf

│

├── ros2\_ws/

│   ├── src/

│   │   └── sentry\_camera/

│   │       ├── config/

│   │       │   └── ekf.yaml

│   │       ├── models/

│   │       │   └── mobile\_robot.urdf

│   │       ├── sentry\_camera/

│   │       │   ├── obstacle\_avoidance.py

│   │       │   ├── target\_controller.py

│   │       │   ├── data\_logger.py

│   │       │   ├── comparison\_logger.py

│   │       │   ├── camera\_publisher.py

│   │       │   └── camera\_subscriber.py

│   │       ├── package.xml

│   │       └── setup.py

│   │

│   ├── worlds/

│   │   └── smart\_bot.world

│   │

│   └── results/

│       ├── plots/

│       ├── simulation\_log.csv

│       ├── comparison\_log.csv

│       └── analyze\_smart\_bot.m

│

└── README.md

```



\## Installation and Setup



\### Prerequisites



\- Ubuntu 22.04 LTS

\- ROS 2 Humble

\- Gazebo Classic 11

\- Python 3

\- MATLAB (optional, for analysis)



\### 1. Clone the repository



```bash

git clone https://github.com/challabhavithsai0123-cell/adaptive-mobile-robot.git

```



\### 2. Navigate to the ROS 2 workspace



```bash

cd adaptive-mobile-robot/ros2\_ws

```



\### 3. Source ROS 2



```bash

source /opt/ros/humble/setup.bash

```



\### 4. Install dependencies



```bash

rosdep install --from-paths src --ignore-src -r -y

```



\### 5. Build the workspace



```bash

colcon build --symlink-install

```



\### 6. Source the workspace



```bash

source install/setup.bash

```



\### 7. Run the simulation



Start Gazebo Classic with ROS integration, load the `worlds/smart\_bot.world` environment, and spawn the robot using `src/sentry\_camera/models/mobile\_robot.urdf`.



Run the obstacle avoidance node after the robot and LiDAR topics are available:



```bash

ros2 run sentry\_camera obstacle\_avoidance

```



Other available package executables include:



```bash

ros2 run sentry\_camera data\_logger

ros2 run sentry\_camera target\_controller

```



The EKF configuration is available at `src/sentry\_camera/config/ekf.yaml`. The `robot\_localization` package must be installed and configured to run the EKF node.



\## Simulation Results



The project records robot trajectories, velocities, obstacle distances and localization measurements.



\### Robot Trajectory



!\[Robot Trajectory](ros2\_ws/results/plots/trajectory.png)



\### Linear Velocity



!\[Linear Velocity](ros2\_ws/results/plots/linear\_velocity.png)



\### Angular Velocity



!\[Angular Velocity](ros2\_ws/results/plots/angular\_velocity.png)



\### LiDAR Obstacle Distance



!\[LiDAR Distance](ros2\_ws/results/plots/lidar\_distance.png)



Additional localization and comparison plots are available in the `ros2\_ws/results/` directory.



\## MATLAB Analysis



The MATLAB script:



```text

ros2\_ws/results/analyze\_smart\_bot.m

```



performs analysis of recorded comparison data, including:



\- Ground-truth trajectory versus wheel odometry and EKF estimates.

\- Localization error comparison.

\- Linear velocity.

\- Angular velocity.

\- Nearest obstacle distance.



\## Project Scope and Limitations



This is a software-based robotics simulation project. The robot, LiDAR and IMU are simulated in Gazebo; no physical STM32 controller or real-world sensor hardware is claimed as part of this simulation.



The architecture and control concepts provide a foundation for future embedded hardware implementation and real-world testing.



\## Future Improvements



\- Integration with an STM32-based embedded controller.

\- Hardware-in-the-loop testing.

\- Real LiDAR and IMU sensor integration.

\- Advanced path planning algorithms.

\- Improved localization and autonomous navigation.

\- Wireless telemetry and live monitoring.



\## Author



\*\*Bhavith Sai\*\*



B.Tech Student | Robotics and Embedded Systems Enthusiast



GitHub: \[challabhavithsai0123-cell](https://github.com/challabhavithsai0123-cell)



\---



If you find this project interesting, feel free to explore the source code and simulation results.



