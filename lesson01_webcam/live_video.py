import cv2
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

print("Live video started. Press q to quit.")

frame_count = 0
start_time = time.time()

while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Failed to capture frame.")
        break

    frame_count += 1

    elapsed_time = time.time() - start_time

    if elapsed_time >= 1.0:
        fps = frame_count / elapsed_time
        print(f"Processing speed: {fps:.2f} FPS")

        frame_count = 0
        start_time = time.time()

    cv2.imshow("SENTRY-ROS - Live Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
print("Camera released.")
