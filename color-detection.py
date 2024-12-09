import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from models.color_model import ColorPicker


def get_image():
    '''Get the selected image information'''
    img_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All Files", "*.*")]
    )

    if not img_path:
        print("No file selected. Exiting...")
        exit()

    img = cv2.imread(img_path)
    if img is None:
        print("Failed to load the image. Please check the file.")
        exit()

    return img

def main():
    root = tk.Tk()
    root.withdraw()

    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('./data/colors_dataset.csv', names=index, header=None)
    img = get_image()

    csv.loc

    picker = ColorPicker(img, csv)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', picker.draw)

    while True:

        cv2.imshow("image", picker.img)
        cv2.waitKey(20)
        if (picker.clicked):
            cv2.rectangle(picker.img, (20,20), (750,60), picker.get_rgb('bgr'), -1)

            print_text(picker, (255,255,255))

            # For light colours we will display text in black
            if(sum(picker.color_rgb) >= 600):
                print_text(picker, (0,0,0))
                
            picker.clicked=False

        #Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
  
    cv2.destroyAllWindows()

def print_text(picker, color):
    cv2.putText(img=picker.img,
                        text=str(picker), 
                        org=(50,50), 
                        fontFace=2, 
                        fontScale=0.8, 
                        color=color, 
                        thickness=2, 
                        lineType=cv2.LINE_AA
                        )

if __name__ == "__main__":
    main()
