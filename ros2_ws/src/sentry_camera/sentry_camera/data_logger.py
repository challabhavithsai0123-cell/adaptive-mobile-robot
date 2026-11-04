#!/usr/bin/env python3
import csv
import math
import os
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


class DataLogger(Node):
    def __init__(self):
        super().__init__('simulation_data_logger')

        folder = os.path.expanduser(
            '~/sentry_ros_v2/ros2_ws/results'
        )
        os.makedirs(folder, exist_ok=True)

        self.file = open(
            os.path.join(folder, 'simulation_log.csv'),
            'w',
            newline=''
        )

        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'time_s', 'x_m', 'y_m', 'linear_velocity_mps',
            'angular_velocity_radps', 'nearest_front_obstacle_m'
        ])

        self.start_time = self.get_clock().now()
        self.latest_scan = None
        self.latest_odom = None

        self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )

        self.create_timer(0.1, self.record_data)
        self.get_logger().info(
            'Logging simulation data to results/simulation_log.csv'
        )

    def scan_callback(self, msg):
        self.latest_scan = msg

    def odom_callback(self, msg):
        self.latest_odom = msg

    def record_data(self):
        if self.latest_scan is None or self.latest_odom is None:
            return

        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        scan = self.latest_scan
        front = []

        for i, distance in enumerate(scan.ranges):
            angle = scan.angle_min + i * scan.angle_increment

            if abs(angle) <= math.radians(30):
                if math.isinf(distance) and distance > 0:
                    front.append(scan.range_max)
                elif math.isfinite(distance) and scan.range_min <= distance <= scan.range_max:
                    front.append(distance)

        nearest = min(front) if front else float('nan')
        odom = self.latest_odom

        self.writer.writerow([
            round(elapsed, 3),
            odom.pose.pose.position.x,
            odom.pose.pose.position.y,
            odom.twist.twist.linear.x,
            odom.twist.twist.angular.z,
            nearest
        ])
        self.file.flush()

    def destroy_node(self):
        self.file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DataLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
