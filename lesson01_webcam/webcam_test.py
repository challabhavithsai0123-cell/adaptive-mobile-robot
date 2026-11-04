
import cv2

# Open the default camera (usually /dev/video0).
camera = cv2.VideoCapture(0)

# Check whether the camera opened successfully.
if not camera.isOpened():
    print("ERROR: Could not open the webcam.")
    exit()

print("Webcam opened successfully.")
print("Press q in the video window to quit.")

while True:
    # Capture one frame from the camera.
    success, frame = camera.read()

    # Stop if a frame could not be captured.
    if not success:
        print("ERROR: Could not read a camera frame.")
        break

    # Display the captured frame.
    cv2.imshow("SENTRY-ROS v2 - Webcam Test", frame)

    # Wait briefly for a key press.
    key = cv2.waitKey(1) & 0xFF

    # Quit when the q key is pressed.
    if key == ord("q"):
        break

# Release the camera and close the display window.
camera.release()
cv2.destroyAllWindows()

print("Webcam test finished.")
