from setuptools import setup, find_packages

setup(
    name='databasetools',
    version='0.3.9',
    packages=find_packages(),
    install_requires=[
              'looptools',
              'mysql-connector==2.1.6',
              'numpy',
              'pandas',
              'tqdm',
          ],
    url='https://github.com/mrstephenneal/databasetools.git',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='A collection of database tools written in Python for handling basic actions with CSV files, '
                'numpy dictionaries, SQLite databases and MySQL databases.'
)
