import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')

load_dotenv(dotenv_path=dotenv_path)

class Config:
    """Base configuration class. Contains default settings."""

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # --- General Flask Settings ---
    DEBUG = False
    TESTING = False

    # --- SQLAlchemy Settings ---
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # --- Email Settings ---
    MAIL_ENABLED = os.getenv('MAIL_ENABLED', 'True').lower() in ('true', '1', 't')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
    MAIL_DEFAULT_SENDER = ('GreenTech Systems', MAIL_USERNAME) if MAIL_USERNAME else None


    # --- Logging ---
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO').upper()


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_ECHO = False



class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False
    SQLALCHEMY_ECHO = False

    if not Config.SECRET_KEY or Config.SECRET_KEY == 'you-really-should-set-a-secret-key':
        pass
    if not Config.SQLALCHEMY_DATABASE_URI:
        pass
    if Config.MAIL_ENABLED and (not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD):
        pass

class TestingConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    MAIL_ENABLED = False
    WTF_CSRF_ENABLED = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)

def get_config():
    """Gets the configuration class based on FLASK_ENV environment variable."""
    env_name = os.getenv('FLASK_ENV', 'default').lower()
    config_class = config_by_name.get(env_name, DevelopmentConfig)

    if config_class == ProductionConfig:
        secret_key = getattr(config_class, 'SECRET_KEY', None)
        db_uri = getattr(config_class, 'SQLALCHEMY_DATABASE_URI', None)
        mail_enabled = getattr(config_class, 'MAIL_ENABLED', False)
        mail_user = getattr(config_class, 'MAIL_USERNAME', None)
        mail_pass = getattr(config_class, 'MAIL_PASSWORD', None)

        if not secret_key:
            raise ValueError("CRITICAL: No SECRET_KEY configured for production environment.")
        if not db_uri:
            raise ValueError("CRITICAL: No DATABASE_URL configured for production environment.")
        if mail_enabled and (not mail_user or not mail_pass):
             raise ValueError("CRITICAL: Mail is enabled but MAIL_USERNAME or MAIL_PASSWORD are not set for production.")

    return config_class