from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_db_args

__all__ = ['eng', 'Base', 'Session']


def get_engine():
    dbargs = get_db_args()
    connect_str = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(dbargs['user'], dbargs['password'],
                                                                       dbargs['host'], dbargs['port'],
                                                                       dbargs['dbname'])  # mysql
    engine = create_engine(connect_str, encoding='utf-8')
    return engine


eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
# db_session = Session()
