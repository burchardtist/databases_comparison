import random
import string
from datetime import timedelta, datetime

from sqlalchemy import create_engine

from settings import DATABASES, TABLE_COLUMNS, TABLE_NAME, QUERIES


def print_range(length):
    for i in range(length):
        print('GENERATING: {0} / {1}'.format(i + 1, length), end='\r')
        yield


class Connector:
    def __init__(self, dbsystem):
        self.dbsystem = dbsystem.upper()

        self.QUERIES = QUERIES[self.dbsystem]
        self.TABLE_COLUMNS = TABLE_COLUMNS[self.dbsystem]
        self.config = DATABASES[self.dbsystem]

        self.conn = self.get_engine()

    def get_engine(self, with_db=True):
        if self.dbsystem == 'SQLITE':
            url = '{db}:///{dbname}'.format(
                db=self.config['CONN'],
                dbname='{}.db'.format(self.config['NAME'])
            )
            return create_engine(url)
        else:
            url = '{db}://{user}:{passwd}@{host}{dbname}'.format(
                db=self.config['CONN'],
                user=self.config['USER'],
                passwd=self.config['PASSWD'],
                host=self.config['HOST'],
                dbname='/{}'.format(self.config['NAME']) if with_db else ''
            )
            return create_engine(url, isolation_level='AUTOCOMMIT' if not with_db else 'READ_COMMITTED')


class Recreate:
    def __init__(self, dbsystems):
        self.dbsystems = dbsystems

    def recreate_db(self, length):
        for db in self.dbsystems:
            self._recreate_db(db)

        self.insert_data(length)

    def _recreate_db(self, db):
        if db.dbsystem == 'SQLITE':
            db.conn = db.get_engine()
            db.conn.execute(db.QUERIES['drop_table'].format(TABLE_NAME))
        else:
            create_conn = db.get_engine(with_db=False)
            create_conn.execute(db.QUERIES['drop_db'].format(db.config['NAME']))
            create_conn.execute(db.QUERIES['create_db'].format(db.config['NAME']))
            db.conn = db.get_engine()
        columns = ''.join(['{} {},'.format(x, z) for x, z in db.TABLE_COLUMNS.items()])[:-1]
        db.conn.execute(db.QUERIES['create_table'].format(TABLE_NAME, columns))

    def insert_data(self, length):
        print('generating data')
        data = [
            dict(
                city=self._gen_city(),
                lat=self._gen_lat(),
                lon=self._gen_lon(),
                date=self._gen_date())
            for _ in print_range(length)
        ]

        for i, name in self._insert_data(data):
            print('[{2}]INSERT: {0} / {1}'.format(i + 1, length, name), end='\r')

    def _insert_data(self, data):
        for connector in self.dbsystems:
            for i, item in enumerate(data):
                connector.conn.execute(connector.QUERIES['insert'].format(
                    TABLE_NAME,
                    ','.join([x for x in item]),
                    ','.join([self.escape_values(col, val) for col, val in item.items()])
                ))
                yield i, connector.dbsystem
            print('')

    def _gen_city(self):
        length = random.randint(3, 50)
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _gen_lat(self):
        return round(random.uniform(-90.0, 90.0), 10)

    def _gen_lon(self):
        return round(random.uniform(-180.0, 180.0), 10)

    def _gen_date(self):
        d1 = datetime.strptime('1/1/2000 12:00 AM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2010 12:00 AM', '%m/%d/%Y %I:%M %p')

        delta = d2 - d1
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return d1 + timedelta(seconds=random_second)

    def escape_values(self, col, val):
        if col in ['lat', 'lon']:
            return str(val)
        else:
            return '\'{}\''.format(val)

if __name__ == '__main__':
    db = Recreate([
        Connector('sqlite'),
        Connector('postgresql'),
        Connector('mysql')
    ])
    db.recreate_db(pow(10, 2))

