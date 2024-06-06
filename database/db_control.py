from peewee import SqliteDatabase

from config_data.config import DB_PATH


db_sqlite = SqliteDatabase(f'{DB_PATH}', pragmas=(
                                                          ('cache_size', -16000),
                                                          ('journal_mode', 'wal'),
                                                           )
                           )
