import os
import csv as csv_builtin
import inspect


class CSV:
    @staticmethod
    def write(data, file_path=None):
        """
        Export data to CSV file.

        :param data: Either a list of tuples or a list of lists.
        :param cols: List of column names, must be the same length as rows within data.
        :param file_path: String of path to save location directory.
        :param file_name: name of file without suffix ('yourfilename' not 'yourfilename.csv').
        """
        # Set file path and name
        if file_path is None:
            file_path = os.path.join(os.getcwd(), get_calling_file())

        with open(file_path, 'w') as write:
            wr = csv_builtin.writer(write)
            wr.writerows(data)
        return file_path

    @staticmethod
    def read(file_name):
        """
        Reads CSV file and returns list of contents

        :param file_name: Path to csv file
        """
        assert os.path.isfile(file_name), 'No such file exists: ' + str(file_name)
        with open(file_name, 'r') as f:
            reader = csv_builtin.reader(f)
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
        if cols:
            data.insert(0, cols)
        file_path = os.path.join(file_path, file_name) if file_name else file_path
        CSV.write(data, file_path)


class CSVImport:
    def __init__(self, file_name):
        CSV.read(file_name)
