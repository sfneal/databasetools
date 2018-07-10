import numpy as np

class NPY:
    """
    Save and load Python dictionaries in numpy .npy format
    """
    def __init__(self, save_path):
        self.save_name = save_path

    def save(self, data_dict):
        np.save(self.save_name, data_dict)

    def load(self):
        read_dictionary = np.load(self.save_name).item()
        return dict(read_dictionary)
