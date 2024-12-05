import argparse
import cv2

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Try loading the image
img = cv2.imread(img_path)
if img is None:
    print("Error: Image not found.")
    exit()

# Display image to check if cv2.imshow() works
cv2.imshow("image", img)

# Wait until any key is pressed
cv2.waitKey(0)

# Destroy all windows after key press
cv2.destroyAllWindows()
