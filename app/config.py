import os

pg_db_username = 'postgres'
pg_db_password = 'Qwerty123'
pg_db_name = 'Tickets'
pg_db_hostname = 'localhost'
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', """#DM?*;C6a{cBbsA.e>A"%Vhnc2>Ctc<e}6S4~?m$f9.~d);&AG""")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                            DB_PASS=pg_db_password,
                                                                                            DB_ADDR=pg_db_hostname,
                                                                                            DB_NAME=pg_db_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                            DB_PASS=pg_db_password,
                                                                                            DB_ADDR=pg_db_hostname,
                                                                                            DB_NAME=pg_db_name)
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
)

key = Config.SECRET_KEY
