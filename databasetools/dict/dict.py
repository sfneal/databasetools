import os
from pprint import pprint
from databasetools.dict.json import JSON
from databasetools.dict.npy import NPY
from databasetools.dict.pickle import Pickle


class DictTools:
    def __init__(self, directory, name, protocol='json'):
        """
        Save or load data to or from .npy dictionary file
        :param directory: Directory to save or load file from
        :param name: File name
        :param protocal: Method for saving and loading dictionaries
        """
        # Get dictionary of protocals
        protocols_dict = self.protocol_options()
        self.choice = protocol.strip('.')  # Remove leading '.' if included in protocal var
        try:
            self.protocol = protocols_dict[self.choice]
        except KeyError:
            # Use Numpy as default
            self.protocol = protocols_dict['json']
        # Join root directory and save name to create full path
        self.save_name = os.path.join(directory, str(name + self.protocol['ext']))
        print(self.protocol)

    def __iter__(self):
        return iter(self.read_dictionary)

    @property
    def choices(self):
        """
        Print dictionary of protocal choices for reference
        :return: protocals dictionary
        """
        protocols_dict = self.protocal_options()
        pprint(protocols_dict)
        return protocols_dict

    @staticmethod
    def protocol_options():
        protocols_dict = {
            'npy': {
                'class': NPY,
                'ext': '.npy'
            },
            'pickle': {
                'class': Pickle,
                'ext': '.p'
            },
            'json': {
                'class': JSON,
                'ext': '.json'
            },
        }
        return protocols_dict

    def save(self, data_dict):
        try:
            dict_class = self.protocol['class']
            dict_class(self.save_name).save(data_dict)
            print("\n" + self.choice + " saved to " + self.save_name)
        except:
            print("\n" + self.choice + " not saved")

    @property
    def load(self):
        try:
            dict_class = self.protocol['class']
            read_dictionary = dict_class(self.save_name).load()
            return read_dictionary
        except IOError:
            print('\nError: Unable to load file ' + str(self.save_name))

