from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode


def get_column_value_strings(columns, query_type='insert'):
    cols = ""
    vals = ""
    if query_type == 'insert':
        for c in columns:
            cols = cols + c + ', '
            vals = vals + '%s' + ', '

        # Remove last comma and space
        cols = cols[:-2]
        vals = vals[:-2]
        return cols, vals
    if query_type == 'update':
        for c in columns:
            cols = str(cols + c + '=%s, ')

        # Remove last comma and space
        cols = cols[:-2]
        return cols


def join_columns(cols):
    return ", ".join([i for i in cols])


class MySQLTools:
    def __init__(self, config, enable_printing=True):
        """
        Connect to MySQL database and execute queries
        :param config: MySQL server configuration settings
        """
        self.enable_printing = enable_printing
        self._cursor = None
        self._cnx = None
        self._connect(config)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._commit()
        self._close()

    def _connect(self, config):
        """Establish a connection with a MySQL database."""
        try:
            self._cnx = mysql.connector.connect(**config)
            self._cursor = self._cnx.cursor()
            self._printer('\tMySQL DB connection established')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            raise err

    def _printer(self, msg):
        """Printing method for internal use."""
        if self.enable_printing:
            print(msg)

    def _close(self):
        """Close MySQL database connection."""
        self._cursor.close()
        self._cnx.close()

    def _commit(self):
        """Commit the changes made during the current connection."""
        self._cnx.commit()

    def _fetch(self, statement):
        """Execute a SQL query and return values."""
        # Execute statement
        self._cursor.execute(statement)
        self._printer('\tMySQL rows successfully queried')
        return [row for row in self._cursor]

    def select(self, table, cols):
        """Query only certain columns from a table and every row."""
        # Concatenate statement
        cols_str = join_columns(cols)
        statement = ("SELECT " + cols_str + " FROM " + str(table))
        return self._fetch(statement)

    def select_where(self, table, cols, where):
        """Query certain columns from a table where a particular value is found."""
        # Either join list of columns into string or set columns to * (all)
        if isinstance(cols, list):
            cols_str = join_columns(cols)
        else:
            cols_str = "*"

        # Unpack WHERE clause dictionary into tuple
        where_col, where_val = where

        statement = ("SELECT " + cols_str + " FROM " + str(table) + ' WHERE ' + str(where_col) + '=' + str(where_val))
        self._fetch(statement)

    def select_all(self, table):
        """Query all rows and columns from a table."""
        # Concatenate statement
        statement = ("SELECT * FROM " + str(table))
        return self._fetch(statement)

    def select_all_join(self, table1, table2, key):
        """Left join all rows and columns from two tables where a common value is shared."""
        # TODO: Write function to run a select * left join query
        pass

    def insert(self, table, columns, values):
        """Insert a singular row into a table"""
        # Concatenate statement
        cols, vals = get_column_value_strings(columns)
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self._cursor.execute(statement, values)
        self._printer('\tMySQL row successfully inserted')

    def insert_many(self, table, columns, values):
        """
        Insert multiple rows into a table.

        If only one row is found, self.insert method will be used.
        """
        # Use self.insert if only one row is being inserted
        if len(values) < 2:
            self.insert(table, columns, values)
        else:
            # Concatenate statement
            cols, vals = get_column_value_strings(columns)
            statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

            # Execute statement
            self._cursor.executemany(statement, values)
            self._printer('\tMySQL rows (' + str(len(values)) + ') successfully INSERTED')

    def update(self, table, columns, values, where):
        """Update the values of a particular row where a value is met."""
        where_col, where_val = where  # Unpack WHERE clause dictionary into tuple
        cols = get_column_value_strings(columns, query_type='update')  # Get SET clause string

        # Concatenate statement
        statement = ("UPDATE " + str(table) + " SET " + str(cols) + ' WHERE ' + str(where_col) + '=' + str(where_val))

        # Execute statement
        self._cursor.execute(statement, values)
        self._printer('\tMySQL rows (' + str(len(values)) + ') successfully UPDATED')

    def truncate(self, table):
        """Empty a table by deleting all of its rows."""
        statement = "TRUNCATE " + str(table)
        self._cursor.execute(statement)
        self._printer('\tMySQL table ' + str(table) + ' successfully truncated')
