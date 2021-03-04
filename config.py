POSTGRES_URL = ''
POSTGRES_USER = ''
POSTGRES_PASSWORD = ''
POSTGRES_DB = ''


class Config(object):
    DEBUG = False
    TESTING = False
    # SQLAlchemy
    uri_template = 'postgresql+psycopg2://{user}:{pw}@{url}/{dbadmin}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PASSWORD,
        url=POSTGRES_URL,
        db=POSTGRES_DB)

    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API settings
    API_PAGINATION_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True


def get_config(env=None):
    env = 'development'
    return DevelopmentConfig()
