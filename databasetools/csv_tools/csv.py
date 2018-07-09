import os
import csv
from pandas.io.parsers import read_csv
from pandas import DataFrame
from pathlib import Path
import inspect


class CSVExport:
    def __init__(self, data=None, cols=None, file_path=None, file_name=None):
        """
        Export data to CSV file.
        :param data: Either a list of tuples or a list of lists.
        :param cols: List of column names, must be the same length as rows within data.
        :param file_path: String of path to save location directory.
        :param file_name: name of file without suffix ('yourfilename' not 'yourfilename.csv').
        """
        self.data = data
        self.cols = cols
        if file_path is None:
            file_path = os.getcwd()
        if file_name is None:
            file_name = get_calling_file()

        self.file_name = Path(os.path.join(file_path, str(file_name + '.csv')))
        self.data_to_csv()

    def __str__(self):
        return str(self.file_name)

    def data_to_csv(self):
        df = DataFrame(self.data, columns=self.cols)
        df.to_csv(self.file_name, index=False)


class CSVImport:
    def __init__(self, file_name):
        """
        Import csv file as list
        :param file_name:
        """
        self.file_name = file_name
        self.data = list
        self.csv_to_list()

    @property
    def list(self):
        return list(self.data)

    def csv_to_list(self):
        """
        Reads CSV file and returns list of contents
        """
        try:
            with open(self.file_name, 'r') as f:
                reader = csv.reader(f)
                self.data = list(reader)
        except FileNotFoundError:
            print('No such file exists: ' + str(self.file_name))


def remove_empty_cols(csv_file):
    """
    Remove empty columns from CSV file
    """
    data = read_csv(csv_file)
    filtered_data = data.dropna(axis='columns', how='all')
    filtered_data.to_csv(csv_file)


def get_calling_file(file_path=None, result='name'):
    """
    Retrieve file_name or file_path of calling Python script
    """
    # Get full path of calling python script
    if file_path is None:
        path = inspect.stack()[1][1]
    else:
        path = file_path

    name = path.split('/')[-1].split('.')[0]
    if result == 'name':
        return name
    elif result == 'path':
        return path
    else:
        return path, name
