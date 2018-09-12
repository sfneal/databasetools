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
        self.cursor = None
        self.cnx = None
        self.connect(config)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def connect(self, config):
        try:
            self.cnx = mysql.connector.connect(**config)
            self.cursor = self.cnx.cursor()
            if self.enable_printing:
                print('\tMySQL DB connection established')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            raise err

    def fetch(self, statement):
        # Execute statement
        self.cursor.execute(statement)
        rows = [row for row in self.cursor]
        if self.enable_printing:
            print('\tMySQL rows successfully queried')
        return rows

    def select(self, table, cols):
        # Concatenate statement
        cols_str = join_columns(cols)
        statement = ("SELECT " + cols_str + " FROM " + str(table))
        return self.fetch(statement)

    def select_where(self, table, cols, where):
        # Either join list of columns into string or set columns to * (all)
        if isinstance(cols, list):
            cols_str = join_columns(cols)
        else:
            cols_str = "*"

        # Unpack WHERE clause dictionary into tuple
        where_col, where_val = where

        statement = ("SELECT " + cols_str + " FROM " + str(table) + ' WHERE ' + str(where_col) + '=' + str(where_val))
        self.fetch(statement)

    def select_all(self, table):
        # Concatenate statement
        statement = ("SELECT * FROM " + str(table))
        return self.fetch(statement)

    def select_all_join(self, table1, table2, key):
        # TODO: Write function to run a select * left join query
        pass

    def insert(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self.cursor.execute(statement, values)
        if self.enable_printing:
            print('\tMySQL row successfully inserted')

    def insert_many(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self.cursor.executemany(statement, values)

        if self.enable_printing:
            print('\tMySQL rows (' + str(len(values)) + ') successfully INSERTED')

    def update(self, table, columns, values, where):
        where_col, where_val = where  # Unpack WHERE clause dictionary into tuple
        cols = get_column_value_strings(columns, query_type='update')  # Get SET clause string

        # Concatenate statement
        statement = ("UPDATE " + str(table) + " SET " + str(cols) + ' WHERE ' + str(where_col) + '=' + str(where_val))

        # Execute statement
        self.cursor.execute(statement, values)
        if self.enable_printing:
            print('\tMySQL rows (' + str(len(values)) + ') successfully UPDATED')

    def truncate(self, table):
        statement = "TRUNCATE " + str(table)
        self.cursor.execute(statement)
        if self.enable_printing:
            print('\tMySQL table ' + str(table) + ' successfully truncated')

    def commit(self):
        self.cnx.commit()

    def close(self):
        self.cursor.close()
        self.cnx.close()
