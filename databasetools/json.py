import json


class JSON:
    """Save and load Python dictionaries in JSON .json format"""
    def __init__(self, save_path):
        self.save_name = str(save_path) if str(save_path).endswith('.json') else str(save_path) + '.json'

    def write(self, data, sort_keys=True, indent=4):
        with open(self.save_name, 'w') as fp:
            json.dump(data, fp, sort_keys=sort_keys, indent=indent)

    def read(self):
        with open(self.save_name, 'r') as fp:
            read_dictionary = json.load(fp)
            return read_dictionary
