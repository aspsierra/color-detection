import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

class ColorPicker:
    def __init__(self, img, color_data):
        self.img = img
        self.color_data = color_data
        self.clicked = False
        self.color_rgb =[0, 0, 0] #! [R, G, B]
        self._position = {'x': 0, 'y': 0}

    @property
    def position(self):
        print(f'''({self._position['x'], self._position['y']})''')
        return self._position
        
    @position.setter
    def position(self, value):
        self._position['x'] = value[0]
        self._position['y'] = value[1]

    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clicked = True
            self.position = (x, y)
            self.set_color_rgb(self.img[y,x], 'bgr')


    def get_rgb(self, format=''):
        '''Retrieve the selected color in different formats'''
        if format == 'r':
            return self.color_rgb[0]
        elif format == 'g':
            return self.color_rgb[1]
        elif format == 'b':
            return self.color_rgb[2]
        elif format == 'bgr':
            print((self.color_rgb[2], self.color_rgb[1], self.color_rgb[0]))
            return (self.color_rgb[2], self.color_rgb[1], self.color_rgb[0])
        else:
            return (self.color_rgb[0], self.color_rgb[1], self.color_rgb[2])

    def set_color_rgb(self, values, format=''):
        if format == 'bgr':
            self.color_rgb = [values[2],values[1],values[0]]
            return
        
        self.color_rgb = values
        

# def draw(event, x, y, flags, param):
#     picker = param['picker']
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         picker.clicked = True
#         picker.position['x'] = x
#         ypos = y
#         b, g, r = img[y, x]

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

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
        #if (picker.clicked):

            #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
            #cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #     #Creating text string to display( Color name and RGB values )
        #     text = get_color_name(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            
        #     #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        #     cv2.putText(img=picker.img,
        #                 text=text, 
        #                 start=(50,50), 
        #                 fontFace=2, 
        #                 fontScale=0.8, 
        #                 color=(255,255,255), 
        #                 thickness=2, 
        #                 lineType=cv2.LINE_AA
        #                 )

        #     #For very light colours we will display text in black colour
        #     if(sum(picker.color_rgb) >= 600):
        #         cv2.putText(
        #             img=img, 
        #             text=text, 
        #             start=(50,50),
        #             fontFace=2, 
        #             fontScale=0.8, 
        #             color=(0,0,0), 
        #             thickness=2, 
        #             lineType=cv2.LINE_AA)
                
        #     picker.clicked=False

        #Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
  
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
