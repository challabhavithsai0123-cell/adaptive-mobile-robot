#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )

        self.avoiding = False
        self.turn_direction = -1.0
        self.last_scan_time = self.get_clock().now()

        self.timer = self.create_timer(0.2, self.check_timeout)
        self.get_logger().info('Reactive LiDAR obstacle avoidance started')

    def sector_values(self, msg, low, high):
        values = []

        for i, distance in enumerate(msg.ranges):
            angle = math.degrees(
                msg.angle_min + i * msg.angle_increment
            )

            if low <= angle <= high:
                if math.isinf(distance) and distance > 0:
                    distance = msg.range_max

                if math.isfinite(distance) and msg.range_min <= distance <= msg.range_max:
                    values.append(distance)

        return values

    def clearance(self, values):
        if not values:
            return 0.0

        values = sorted(values)
        index = int(0.20 * (len(values) - 1))
        return values[index]

    def scan_callback(self, msg):
        self.last_scan_time = self.get_clock().now()

        front = self.sector_values(msg, -25, 25)
        left = self.sector_values(msg, 35, 100)
        right = self.sector_values(msg, -100, -35)

        cmd = Twist()

        if not front:
            self.publisher.publish(cmd)
            self.get_logger().warning('No front LiDAR data: STOP')
            return

        front_distance = min(front)

        left_clearance = self.clearance(left)
        right_clearance = self.clearance(right)

        if not self.avoiding and front_distance < 0.80:
            self.avoiding = True
            self.turn_direction = (
                1.0 if left_clearance > right_clearance else -1.0
            )

            self.get_logger().info(
                f'Obstacle {front_distance:.2f} m | '
                f'Left {left_clearance:.2f} m | '
                f'Right {right_clearance:.2f} m | '
                f'Turning {"LEFT" if self.turn_direction > 0 else "RIGHT"}'
            )

        if self.avoiding:
            if front_distance > 1.00:
                self.avoiding = False
                self.get_logger().info('Front clear: moving forward')
            else:
                cmd.angular.z = 0.7 * self.turn_direction
                self.publisher.publish(cmd)
                return

        cmd.linear.x = 0.12
        self.publisher.publish(cmd)

    def check_timeout(self):
        age = (
            self.get_clock().now() - self.last_scan_time
        ).nanoseconds / 1e9

        if age > 1.0:
            self.publisher.publish(Twist())
            self.get_logger().warning('LiDAR timeout: STOP')


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            if rclpy.ok():
                node.publisher.publish(Twist())
        except Exception:
            pass

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
