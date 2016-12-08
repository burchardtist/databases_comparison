import random
import string
from datetime import timedelta, datetime

from sqlalchemy import create_engine
from sqlalchemy import text

from settings import DATABASES, TABLE_COLUMNS, TABLE_NAME, QUERIES, DB_SIZE
from setup_logger import setup_logger
from timed import Timed


logger = setup_logger('performance')


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
    def __init__(self, dbsystems, length):
        self.dbsystems = dbsystems
        self.data = self.generate_data(length)
        print('')
        self.length = len(self.data)
        logger.info('LENGTH: {}'.format(self.length))

    def recreate_db(self):
        for connector in self.dbsystems:
            self._recreate_db(connector)

    def close(self):
        for connector in self.dbsystems:
            connector.conn.dispose()

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

    def generate_data(self, length):
        print('generating data')
        return [
            dict(
                city=self._gen_city(),
                lat=self._gen_lat(),
                lon=self._gen_lon(),
                date=self._gen_date())
            for _ in print_range(length)
        ]

    @Timed('insert')
    def insert_data(self, **kwargs):
        for connector in self.dbsystems:
            for i, name in self._insert_data(self.data, connector):
                print('[INSERT][{2}]: {0} / {1}'.format(i + 1, self.length, name), end='\r')
            print('')
            yield connector.dbsystem, self.length

    @Timed('select')
    def select_data(self, where, **kwargs):
        for connector in self.dbsystems:
            connector.conn.execute(text(connector.QUERIES['select'].format(
                TABLE_NAME,
                where
            )))
            yield connector.dbsystem, self.length

    @Timed('update')
    def update_data(self, set_, where, **kwargs):
        for connector in self.dbsystems:
            for i, name in self._update_data(connector, set_, where):
                print('[UPDATE][{2}]: {0} / {1}'.format(i + 1, self.length, name), end='\r')
            print('')
            yield connector.dbsystem, self.length

    def add_index(self):
        for connector in self.dbsystems:
            connector.conn.execute(connector.QUERIES['create_index'].format(
                TABLE_NAME,
                'city',
                'city_index'
            ))
            connector.conn.execute(connector.QUERIES['create_index'].format(
                TABLE_NAME,
                'lat',
                'lat_index'
            ))
            print('[ADD_INDEX][{}] done'.format(connector.dbsystem))

    def _insert_data(self, data, connector):
        for i, item in enumerate(data):
            connector.conn.execute(connector.QUERIES['insert'].format(
                TABLE_NAME,
                ','.join([x for x in item]),
                ','.join([self.escape_values(col, val) for col, val in item.items()])
            ))
            yield i, connector.dbsystem

    def _update_data(self, connector, set_, where):
        for i in range(self.length):
            connector.conn.execute(text(connector.QUERIES['update'].format(
                TABLE_NAME,
                set_,
                where
            )))
            yield i, connector.dbsystem

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
    for length in DB_SIZE:
        for _ in range(5):
            db = Recreate(
                [
                    Connector('sqlite'),
                    Connector('postgresql'),
                    Connector('mysql')
                ],
                length
            )
            db.recreate_db()
            db.insert_data()
            db.select_data('city like \'%ab%\' and lat > 30')
            db.update_data('city=\'1posen\', lat=52.4064, lon=16.9252', 'city like \'%ab%\'')
            db.close()

            db.recreate_db()
            db.add_index()
            db.select_data('city like \'%1pos%\' and lat > 30', indexed=True)
            db.update_data('city=\'stadt\', lat=5.40624, lon=1.3252', 'city like \'%1pos%\'', indexed=True)
            db.insert_data(indexed=True)
            db.close()
