DB_SIZE = [pow(10, 5), pow(10, 7), pow(10, 9)]

DATABASES = dict(
    MYSQL=dict(
        HOST='127.0.0.1',
        USER='root',
        PASSWD='admin123',
        NAME='comparison',
        CONN='mysql+pymysql'
    ),
    POSTGRESQL=dict(
        HOST='127.0.0.1',
        USER='postgres',
        PASSWD='admin123',
        NAME='comparison',
        CONN='postgresql+psycopg2'
    ),
    SQLITE=dict(
        NAME='comparison',
        CONN='sqlite'
    )
)

TABLE_NAME = 'testtable'

TABLE_COLUMNS = {
    'MYSQL': {
        'id': 'int PRIMARY KEY NOT NULL AUTO_INCREMENT',
        'city': 'varchar(255)',
        'lat': 'float(13,10)',
        'lon': 'float(13,10)',
        'date': 'datetime'
    },
    'POSTGRESQL': {
        'id': 'serial PRIMARY KEY NOT NULL',
        'city': 'varchar(255)',
        'lat': 'decimal(13,10)',
        'lon': 'decimal(13,10)',
        'date': 'timestamp'
    },
    'SQLITE': {
        'id': 'integer PRIMARY KEY AUTOINCREMENT',
        'city': 'varchar(255)',
        'lat': 'decimal(13,10)',
        'lon': 'decimal(13,10)',
        'date': 'timestamp'
    }
}

QUERIES = {
    'MYSQL': {
        'create_db': 'CREATE DATABASE {0};',
        'drop_db': 'DROP DATABASE IF EXISTS {0};',
        'create_table': 'CREATE TABLE {0}({1});',
        'insert': 'INSERT INTO {0}({1}) VALUES({2});'
    },
    'POSTGRESQL': {
        'create_db': 'CREATE DATABASE {0};',
        'drop_db': 'DROP DATABASE IF EXISTS {0};',
        'create_table': 'CREATE TABLE {0}({1});',
        'insert': 'INSERT INTO {0}({1}) VALUES({2});'
    },
    'SQLITE': {
        'create_table': 'CREATE TABLE {0}({1});',
        'drop_table': 'DROP TABLE IF EXISTS {0};',
        'insert': 'INSERT INTO {0}({1}) VALUES({2});'
    }
}

