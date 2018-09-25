from setuptools import setup, find_packages

setup(
    name='databasetools',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'mysql-connector>=2.1.6',
        'tqdm',
    ],
    url='https://github.com/mrstephenneal/databasetools',
    license='MIT License',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Convenient data storage toolkit.',
    long_description='A collection of database tools written in Python for handling basic actions with CSV files, '
                'numpy dictionaries, SQLite databases and MySQL databases.'
)

