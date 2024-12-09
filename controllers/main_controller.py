from PyQt5.QtWidgets import QFileDialog
from views.image_view import ImageView
from models.color_model import ColorPicker
import pandas as pd


class MainController:
    def __init__(self):
        # Load color data
        index = ["color", "color_name", "hex", "R", "G", "B"]
        self.color_data = pd.read_csv('./data/colors_dataset.csv', names=index, header=None)
        self.model = ColorPicker(self.color_data)
        self.view = ImageView(self)

    def run(self):
        """Run the application."""
        self.view.open_file_dialog()
        self.view.show()

    def handle_color_selection(self, rgb):
        """Handle color selection and update the view."""
        self.model.find_closest_color(rgb)
        if self.model.selected_color:
            self.view.update_color_label(str(self.model), self.model.selected_color['hex'], self.model.selected_color['text_color'])
