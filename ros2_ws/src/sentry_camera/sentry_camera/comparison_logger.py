#!/usr/bin/env python3

import csv
import math
import os
import rclpy

from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan, Imu
from gazebo_msgs.msg import ModelStates


def get_yaw(q):
    return math.atan2(
        2.0 * (q.w * q.z + q.x * q.y),
        1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    )


class ComparisonLogger(Node):

    def __init__(self):
        super().__init__('comparison_logger')

        self.folder = os.path.expanduser(
            '~/sentry_ros_v2/ros2_ws/results'
        )
        os.makedirs(self.folder, exist_ok=True)

        self.path = os.path.join(
            self.folder, 'comparison_log.csv'
        )

        self.file = open(self.path, 'w', newline='')
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            'time_s',
            'gt_x', 'gt_y', 'gt_yaw',
            'odom_x', 'odom_y', 'odom_yaw',
            'ekf_x', 'ekf_y', 'ekf_yaw',
            'imu_gyro_z',
            'linear_velocity',
            'angular_velocity',
            'nearest_obstacle'
        ])

        self.gt = None
        self.odom = None
        self.ekf = None
        self.imu = None
        self.scan = None

        self.create_subscription(
            ModelStates,
            '/gazebo/model_states',
            self.gt_callback, 10
        )

        self.create_subscription(
            Odometry, '/odom',
            self.odom_callback, 10
        )

        self.create_subscription(
            Odometry, '/odometry/filtered',
            self.ekf_callback, 10
        )

        self.create_subscription(
            Imu, '/imu/data',
            self.imu_callback, 10
        )

        self.create_subscription(
            LaserScan, '/scan',
            self.scan_callback, 10
        )

        self.start_time = self.get_clock().now()

        self.create_timer(0.1, self.record)

        self.get_logger().info(
            'Comparison logger started. Waiting for sensor data...'
        )

    def gt_callback(self, msg):
        try:
            index = msg.name.index('adaptive_mobile_robot')
            pose = msg.pose[index]
            self.gt = (
                pose.position.x,
                pose.position.y,
                get_yaw(pose.orientation)
            )
        except ValueError:
            pass

    def odom_callback(self, msg):
        pose = msg.pose.pose
        self.odom = (
            pose.position.x,
            pose.position.y,
            get_yaw(pose.orientation),
            msg.twist.twist.linear.x,
            msg.twist.twist.angular.z
        )

    def ekf_callback(self, msg):
        pose = msg.pose.pose
        self.ekf = (
            pose.position.x,
            pose.position.y,
            get_yaw(pose.orientation)
        )

    def imu_callback(self, msg):
        self.imu = msg.angular_velocity.z

    def scan_callback(self, msg):
        distances = []

        for distance in msg.ranges:
            if math.isfinite(distance):
                if msg.range_min <= distance <= msg.range_max:
                    distances.append(distance)

        self.scan = min(distances) if distances else float('nan')

    def record(self):
        if any(value is None for value in (
            self.gt, self.odom, self.ekf, self.imu, self.scan
        )):
            return

        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        self.writer.writerow([
            round(elapsed, 3),
            *self.gt,
            *self.odom[:3],
            *self.ekf,
            self.imu,
            self.odom[3],
            self.odom[4],
            self.scan
        ])

        self.file.flush()

    def destroy_node(self):
        self.file.close()
        self.get_logger().info(
            f'Comparison data saved: {self.path}'
        )
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ComparisonLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
