# Migrate SQL databases
from databasetools import MySQLTools


config = {
    "database": "hpa_allin_og",
    "host": "stephenneal.net",
    "password": "Stealth19!",
    "port": 3306,
    "raise_on_warnings": True,
    "user": "stephen_hpa"
}


with MySQLTools(config) as sql:
    # Retrieve list of tables
    t = sql.get_tables()
    print(t, '\n')

