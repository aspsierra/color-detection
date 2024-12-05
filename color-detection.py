import argparse
import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def draw(event, x, y, flag, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)        
        g = int(g)        
        r = int(r)

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname


def main():
    global b, g, r, xpos, ypos, clicked
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('./data/colors_dataset.csv', names=index, header=None)

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

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw)


    while True:

        cv2.imshow("image", img)
        cv2.waitKey(20)
        if (clicked):

            #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
            cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

            #Creating text string to display( Color name and RGB values )
            text = get_color_name(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            
            #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

            #For very light colours we will display text in black colour
            if(r+g+b>=600):
                cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
                
            clicked=False

        #Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
  
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
