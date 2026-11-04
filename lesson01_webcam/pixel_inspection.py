import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

success, frame = camera.read()

if success:
    height, width, channels = frame.shape

    # Find the center pixel of the image.
    y = height // 2
    x = width // 2

    # Read that pixel's color values.
    pixel = frame[y, x]

    print("Image height:", height)
    print("Image width:", width)
    print("Number of channels:", channels)
    print("Center pixel position (x, y):", (x, y))
    print("Center pixel BGR values:", pixel)
else:
    print("ERROR: Could not capture a frame.")

camera.release()
