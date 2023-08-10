class Config:
    SECRET_KEY = 'secret! temporary'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


ConfigsByName = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}