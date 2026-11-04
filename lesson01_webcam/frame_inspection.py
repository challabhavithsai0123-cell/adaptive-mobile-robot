
import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

# Request a camera resolution of 640 x 480 pixels.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Capture one frame.
success, frame = camera.read()

if success:
    print("Frame captured successfully!")

    # Print the image array's dimensions.
    print("Frame shape:", frame.shape)

    # Print the image's data type.
    print("Pixel data type:", frame.dtype)

    # Print the minimum and maximum pixel values.
    print("Minimum pixel value:", frame.min())
    print("Maximum pixel value:", frame.max())

    # Display the captured image.
    cv2.imshow("SENTRY-ROS - Captured Frame", frame)
    cv2.waitKey(0)
else:
    print("ERROR: Failed to capture frame.")

camera.release()
cv2.destroyAllWindows()
