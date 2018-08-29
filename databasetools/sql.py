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


class MySQLTools:
    def __init__(self, config):
        """
        Connect to MySQL database and execute queries
        :param config: MySQL server configuration settings
        """
        self.cursor = None
        self.cnx = None
        self.connect(config)

    def connect(self, config):
        try:
            self.cnx = mysql.connector.connect(**config)
            self.cursor = self.cnx.cursor()
            print('\tMySQL DB connection established')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def select_all(self, table):
        # Concatenate statement
        statement = ("SELECT * FROM " + str(table))

        # Execute statement
        self.cursor.execute(statement)
        rows = [row for row in self.cursor]
        print('\tMySQL rows successfully queired')
        return rows

    def insert(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self.cursor.execute(statement, values)
        print('\tMySQL row successfully inserted')

    def insert_many(self, table, columns, values):
        cols, vals = get_column_value_strings(columns)

        # Concatenate statement
        statement = ("INSERT INTO " + str(table) + "(" + cols + ") " + "VALUES (" + vals + ")")

        # Execute statement
        self.cursor.executemany(statement, values)

        print('\tMySQL rows (' + str(len(values)) + ') successfully INSERTED')

    def update(self, table, columns, values, where):
        where_col, where_val = where  # Unpack WHERE clause dictionary into tuple
        cols = get_column_value_strings(columns, query_type='update')  # Get SET clause string

        # Concatenate statement
        statement = ("UPDATE " + str(table) + " SET " + str(cols) + ' WHERE ' + str(where_col) + '=' + str(where_val))

        # Execute statement
        self.cursor.execute(statement, values)
        print('\tMySQL rows (' + str(len(values)) + ') successfully UPDATED')

    def truncate(self, table):
        statement = "TRUNCATE " + str(table)
        self.cursor.execute(statement)
        print('\tMySQL table ' + str(table) + ' successfully truncated')

    def commit(self):
        self.cnx.commit()

    def close(self):
        self.cursor.close()
        self.cnx.close()
