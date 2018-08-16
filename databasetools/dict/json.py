import json


class JSON:
    """
    Save and load Python dictionaries in JSON .json format
    """
    def __init__(self, save_path):
        self.save_name = save_path

    def write(self, data_dict):
        with open(self.save_name, 'w') as fp:
            json.dump(data_dict, fp, sort_keys=True, indent=4)

    def read(self):
        with open(self.save_name, 'r') as fp:
            read_dictionary = json.load(fp)
            return dict(read_dictionary)
