import numpy as np


class ColorPicker:
    def __init__(self, color_data):
        self.color_data = color_data
        self._selected_color = None
    
    @property
    def selected_color(self):
        return self._selected_color
    
    @selected_color.setter
    def selected_color(self, value):
        self._selected_color = value.to_dict()
        self._selected_color['text_color'] = 'black' if sum((int(self._selected_color['R']),int(self._selected_color['G']),int(self._selected_color['B']))) >= 600 else 'white'


    def find_closest_color(self, rgb):
        """Find the closest color name and hex code for the given RGB values."""
        colors = np.array([
            (self.color_data.loc[i,'R'], 
            self.color_data.loc[i,'G'], 
            self.color_data.loc[i,'B'])
            for i in range(len(self.color_data))
            ])
        selected_color = np.array(rgb)

        # This formula is used to calculate the distance between 2 points in a 
        # 3D space 
        distances = np.sqrt(np.sum((colors - selected_color)**2, axis=1))
        index_smallest = np.argmin(distances)

        self.selected_color = self.color_data.iloc[index_smallest]

    def __str__(self):
        return f'''{self.selected_color['color_name']} Hex={self.selected_color['hex']}'''

