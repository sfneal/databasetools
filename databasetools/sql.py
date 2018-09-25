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
        try:
            self._cnx = mysql.connector.connect(**config)
            self._cursor = self._cnx.cursor()
            self._printer('\tMySQL DB connection established')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self._printer("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self._printer("Database does not exist")
            raise err

    def _printer(self, msg):
        """Printing method for internal use."""
        if self.enable_printing:
            print(msg)

    def _close(self):
        self._cursor.close()
        self._cnx.close()

    def _commit(self):
        self._cnx.commit()

    def _fetch(self, statement):
        # Execute statement
        self._cursor.execute(statement)
        self._printer('\tMySQL rows successfully queried')
        return [row for row in self._cursor]

    def select(self, table, cols):
        # Concatenate statement
        cols_str = join_columns(cols)
        statement = ("SELECT " + cols_str + " FROM " + str(table))
        return self._fetch(statement)

    def select_where(self, table, cols, where):
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
        # Concatenate statement
        statement = ("SELECT * FROM " + str(table))
        return self._fetch(statement)

    def select_all_join(self, table1, table2, key):
        # TODO: Write function to run a select * left join query
        pass

    def insert(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self._cursor.execute(statement, values)
        self._printer('\tMySQL row successfully inserted')

    def insert_many(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self._cursor.executemany(statement, values)
        self._printer('\tMySQL rows (' + str(len(values)) + ') successfully INSERTED')

    def update(self, table, columns, values, where):
        where_col, where_val = where  # Unpack WHERE clause dictionary into tuple
        cols = get_column_value_strings(columns, query_type='update')  # Get SET clause string

        # Concatenate statement
        statement = ("UPDATE " + str(table) + " SET " + str(cols) + ' WHERE ' + str(where_col) + '=' + str(where_val))

        # Execute statement
        self._cursor.execute(statement, values)
        self._printer('\tMySQL rows (' + str(len(values)) + ') successfully UPDATED')

    def truncate(self, table):
        statement = "TRUNCATE " + str(table)
        self._cursor.execute(statement)
        self._printer('\tMySQL table ' + str(table) + ' successfully truncated')
