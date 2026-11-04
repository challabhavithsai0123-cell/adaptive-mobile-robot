import cv2

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')

        # Open the default webcam.
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            raise RuntimeError('Could not open webcam')

        # Convert OpenCV images into ROS image messages.
        self.bridge = CvBridge()

        # Publish images on this ROS 2 topic.
        self.publisher = self.create_publisher(
            Image,
            '/camera/image_raw',
            10
        )

        # Capture and publish a frame every 0.1 seconds.
        self.timer = self.create_timer(0.1, self.publish_frame)

        self.get_logger().info('Camera publisher started')

    def publish_frame(self):
        success, frame = self.camera.read()

        if not success:
            self.get_logger().warning('Could not capture frame')
            return

        image_message = self.bridge.cv2_to_imgmsg(
            frame,
            encoding='bgr8'
        )

        self.publisher.publish(image_message)


def main(args=None):
    rclpy.init(args=args)

    node = None

    try:
        node = CameraPublisher()
        rclpy.spin(node)

    except (RuntimeError, KeyboardInterrupt) as error:
        if isinstance(error, RuntimeError):
            print(f'Camera error: {error}')

    finally:
        if node is not None:
            node.camera.release()
            node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
