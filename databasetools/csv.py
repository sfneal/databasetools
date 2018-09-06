import os
import _csv as csv_builtin
import inspect


class CSV:
    def __init__(self, file_path=None):
        # Set file path and name
        if file_path is None:
            self.file_path = os.path.join(os.getcwd(), get_calling_file())
        else:
            self.file_path = file_path

    def write(self, data, method='w'):
        """
        Export data to CSV file.

        :param data: Either a list of tuples or a list of lists.
        :param method: File opening method.
        """
        # Add .csv file extension
        if not self.file_path.endswith('.csv'):
            self.file_path = self.file_path + '.csv'

        with open(self.file_path, method) as write:
            wr = csv_builtin.writer(write)
            wr.writerows(data)
        return self.file_path

    def append(self, data):
        """Append rows to an existing CSV file"""
        return self.write(data, method='a')

    def read(self):
        """Reads CSV file and returns list of contents"""
        assert os.path.isfile(self.file_path), 'No such file exists: ' + str(self.file_path)
        with open(self.file_path, 'r') as f:
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
