import os
import csv
import inspect


class CSV:
    @staticmethod
    def write(data, cols=None, file_path=None, file_name=None):
        """
        Export data to CSV file.

        :param data: Either a list of tuples or a list of lists.
        :param cols: List of column names, must be the same length as rows within data.
        :param file_path: String of path to save location directory.
        :param file_name: name of file without suffix ('yourfilename' not 'yourfilename.csv').
        """
        # Set file path and name
        if file_path is None:
            file_path = os.getcwd()
        if file_name is None:
            file_name = get_calling_file()

        # Push columns to first row
        if cols is not None:
            data.insert(cols, 0)

        file_name = os.path.join(file_path, str(file_name + '.csv'))

        with open(file_name, 'w') as write:
            wr = csv.writer(write)
            wr.writerows(data)
        return file_name

    @staticmethod
    def read(file_name):
        """
        Reads CSV file and returns list of contents

        :param file_name: Path to csv file
        """
        assert os.path.isfile(file_name), 'No such file exists: ' + str(file_name)
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data


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


# Backward compatibility
class CSVExport:
    def __init__(self, data=None, cols=None, file_path=None, file_name=None):
        CSV.write(data, cols, file_path, file_name)


class CSVImport:
    def __init__(self, file_name):
        CSV.read(file_name)