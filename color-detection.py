import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import numpy as np

root = tk.Tk()
root.withdraw()

class ColorPicker:
    def __init__(self, img, color_data):
        self.img = img
        self.color_data = color_data
        self.selected_color = None
        self.clicked = False
        self.color_rgb =[0, 0, 0] #! [R, G, B]
        self._position = {'x': 0, 'y': 0}

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position['x'] = value[0]
        self._position['y'] = value[1]

    def get_rgb(self, format=''):
        '''Retrieve the selected color in different formats'''
        if format == 'r':
            return self.color_rgb[0]
        elif format == 'g':
            return self.color_rgb[1]
        elif format == 'b':
            return self.color_rgb[2]
        elif format == 'bgr':
            return (self.color_rgb[2], self.color_rgb[1], self.color_rgb[0])
        else:
            return (self.color_rgb[0], self.color_rgb[1], self.color_rgb[2])

    def set_color_rgb(self, values, format=''):
        values = [int(n) for n in values]
        if format == 'bgr':
            self.color_rgb = (values[2], values[1], values[0])
            return
        
        self.color_rgb = values
        
    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clicked = True
            self.position = (x, y)
            self.set_color_rgb(self.img[y,x], 'bgr')
            self.get_color_name()

    def get_color_name(self):
        '''Get the name of the closest color in the csv file'''
        colors = np.array([
            (self.color_data.loc[i,'R'], 
            self.color_data.loc[i,'G'], 
            self.color_data.loc[i,'B'])
            for i in range(len(self.color_data))
            ])
        selected_color = np.array(self.get_rgb())

        # This formula is used to calculate the distance between 2 points in a 
        # 3D space 
        distances = np.sqrt(np.sum((colors - selected_color)**2, axis=1))
        index_smallest = np.argmin(distances)

        self.selected_color = self.color_data.iloc[index_smallest]


    def __str__(self):
        return f'''{self.selected_color['color_name']} Hex={self.selected_color['hex']}'''

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
