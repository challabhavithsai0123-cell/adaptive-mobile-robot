import cv2
import numpy as np
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge


class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridge = CvBridge()

        self.direction_publisher = self.create_publisher(
            String, '/target/direction', 10
        )

        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )

        self.get_logger().info('Green target tracking started')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(
            msg, desired_encoding='bgr8'
        )

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 80, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest) > 500:
                (x, y), radius = cv2.minEnclosingCircle(largest)
                center_x, center_y = int(x), int(y)

                error_x = center_x - 320

                if error_x < -50:
                    direction = 'LEFT'
                elif error_x > 50:
                    direction = 'RIGHT'
                else:
                    direction = 'CENTRE'

                message = String()
                message.data = direction
                self.direction_publisher.publish(message)

                cv2.circle(
                    frame, (center_x, center_y), 5, (255, 0, 0), -1
                )
                cv2.circle(
                    frame, (center_x, center_y), int(radius),
                    (0, 0, 255), 2
                )
                cv2.putText(
                    frame, direction, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
                )

        cv2.imshow('SENTRY-ROS - Target Tracking', frame)
        cv2.imshow('Green Mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
