import rclpy

from rclpy.node import Node
from std_msgs.msg import String


class TargetController(Node):

    def __init__(self):
        super().__init__('target_controller')

        self.last_target_time = None
        self.target_timeout = 1.0
        self.state = 'WAITING'
        self.last_decision = None

        self.direction_subscription = self.create_subscription(
            String,
            '/target/direction',
            self.direction_callback,
            10
        )

        self.command_publisher = self.create_publisher(
            String,
            '/robot/control_command',
            10
        )

        self.safety_timer = self.create_timer(
            0.2,
            self.check_target_timeout
        )

        self.publish_command('STOP')
        self.get_logger().info(
            'Controller started - simulation only'
        )

    def publish_command(self, command):
        message = String()
        message.data = command
        self.command_publisher.publish(message)

    def direction_callback(self, msg):
        direction = msg.data
        self.last_target_time = self.get_clock().now()

        if direction == 'LEFT':
            command = 'TURN_LEFT'
        elif direction == 'RIGHT':
            command = 'TURN_RIGHT'
        elif direction == 'CENTRE':
            command = 'STRAIGHT'
        else:
            command = 'STOP'

        if self.state != 'TRACKING':
            self.state = 'TRACKING'
            self.get_logger().info('State: TRACKING')

        self.publish_command(command)

        if command != self.last_decision:
            self.get_logger().info(
                f'Direction: {direction} | Command: {command}'
            )
            self.last_decision = command

    def check_target_timeout(self):
        if self.last_target_time is None:
            if self.state != 'WAITING':
                self.state = 'WAITING'
                self.get_logger().warning('State: WAITING')

            self.publish_command('STOP')
            return

        elapsed = (
            self.get_clock().now() - self.last_target_time
        ).nanoseconds / 1e9

        if elapsed > self.target_timeout:
            if self.state != 'TARGET_LOST':
                self.state = 'TARGET_LOST'
                self.last_decision = 'STOP'
                self.get_logger().warning(
                    'State: TARGET_LOST | Command: STOP'
                )

            self.publish_command('STOP')


def main(args=None):
    rclpy.init(args=args)
    node = TargetController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
