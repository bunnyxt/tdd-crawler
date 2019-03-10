from functools import wraps, partial
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
# from psycopg2 import IntegrityError as pgIntegrityError
from sqlalchemy.exc import InvalidRequestError
from logger import storagelog


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            storagelog.error('DB operation error，here are details:{}'.format(e))
            args[2].rollback()  # db_session--->args[2]

    return session_commit


class DBOperation:

    @classmethod
    @db_commit_decorator
    def add(cls, data, db_session):
        try:
            db_session.add(data)
            db_session.commit()
        except Exception as e:
            print(e)

    @classmethod
    @db_commit_decorator
    def add_all(cls, datas, db_session):
        try:
            db_session.add_all(datas)
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            # except (SqlalchemyIntegrityError, pgIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add(data, db_session)

    @classmethod
    @db_commit_decorator
    def query(cls, table, db_session):
        try:
            result = db_session.query(table).all()
            return result
        except Exception as e:
            print(e)
