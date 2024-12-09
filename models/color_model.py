import cv2
import pandas as pd
import tkinter as tk
import numpy as np


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

