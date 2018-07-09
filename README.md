# Database Tools

A collection of database tools written in Python for handling basic actions with CSV files, numpy dictionary, SQLite
databases and MySQL databases.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
pip install --upgrade pip
```

### Installing

A step by step series of examples that tell you how to get a development env running

PyPi distribution

```
pip install databasetools
```

## Example Usage

Outlined below are basic uses of the four main classes of the directory utility python package.

* CSVImport - Import csv file as list
* CSVExport - Export data to csv file 
* DictTools - Save or load data to or from .npy dictionary file
* MySQLTools - Connect to MySQL database and execute queries
* PHPArray - Encode data as a sequential or associative PHP array
* SQLiteSyntax - Generate SQLite syntax
* SQLiteQuery - Execute SQLite queries
* SQLiteTools - Generate and execute SQLite queries with a single call

## Built With

* [looptools](https://github.com/mrstephenneal/looptools) - Logging output, timing processes and counting iterations.
* [numpy](http://www.numpy.org/) - Used to save and load .npy files
* [pandas](https://pandas.pydata.org/) - Data structure package used with CSV files
* [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) - Self-container driver for communication with MySQL servers
* [tqdm](https://github.com/tqdm/tqdm) - A fast, extensible progress bar for Python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mrstephenneal/databasetools/contributing.md) for details on our code of
 conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/mrstephenneal/databasetools).

## Authors

* **Stephen Neal** - *Initial work* - [databasetools](https://github.com/mrstephenneal/databasetools)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
