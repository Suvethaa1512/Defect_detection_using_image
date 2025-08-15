import cv2
import time
import os

# DroidCam URL (replace with your DroidCam IP and port)
droidcam_url = "http://192.168.43.1:4747/video"

# Open the video stream
cap = cv2.VideoCapture(droidcam_url)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Interval in seconds (e.g., capture an image every 5 seconds)
interval = 5

# Folder to save images
save_folder = "captured_images"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Counter for image filenames
image_counter = 0

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Save image
        image_name = os.path.join(save_folder, f"image_{image_counter}.jpg")
        cv2.imwrite(image_name, gray_frame)
        print(f"Saved: {image_name}")

        image_counter += 1
        time.sleep(interval)

except KeyboardInterrupt:
    print("Image capture stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Video stream closed.")
