import numpy as np
import os


class DictTools:
    def __init__(self, name):
        """
        Save or load data to or from .npy dictionary file
        :param name: File name
        """
        self.dict = dict
        self.save_name = name + ".npy"

    def __iter__(self):
        return iter(self.read_dictionary)

    def save(self, dict):
        try:
            np.save(self.save_name, dict)
            print("\nnpy saved to " + os.getcwd())
        except:
            print("\nnpy not saved")

    def load(self):
        try:
            self.read_dictionary = np.load(self.save_name).item()
            return self.read_dictionary
        except IOError:
            print('\nError: Unable to load file ' + str(self.save_name))
