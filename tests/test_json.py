import os
import unittest
from tempfile import NamedTemporaryFile
from databasetools import JSON

from looptools import Timer


class TestConduitEncrypt(unittest.TestCase):
    def setUp(self):
        self.temp = NamedTemporaryFile(suffix='.json', delete=False)
        self.json = JSON(self.temp.name)

    def tearDown(self):
        if os.path.exists(self.temp.name):
            os.remove(self.temp.name)

    @Timer.decorator
    def test_write(self):
        data = {'data': list(range(0, 100))}
        self.json.write(data)
        self.assertEqual(self.json.read(), data)

    @Timer.decorator
    def test_read(self):
        data = {'data': list(range(0, 100))}
        self.json.write(data)

        read = self.json.read()
        self.assertEqual(read, data)

    @Timer.decorator
    def test_read_write(self):
        data = {'data': list(range(0, 100))}
        self.json.write(data)

        self.assertEqual(self.json.read(), data)

    @Timer.decorator
    def test_update(self):
        data_1 = {'data': 'foo'}
        self.json.write(data_1)

        data_2 = {'data': 'bar'}
        self.json.update(key='data', data='bar')

        self.assertEqual(self.json.read(), data_2)
        self.assertNotEqual(self.json.read(), data_1)

    @Timer.decorator
    def test_append(self):
        data = {'data': list(range(0, 100))}
        self.json.write(data)
        self.json.append(100, 'data')

        self.assertEqual(self.json.read(), {'data': list(range(0, 101))})


if __name__ == '__main__':
    unittest.main()
