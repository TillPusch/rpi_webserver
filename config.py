
from pathlib import PureWindowsPath

class Config(object):
    DEBUG = False
    TESTING = False
    
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    
    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    
    IMAGE_UPLOADS = "C:/Users/pusch/Documents/python/website/app/static/img/uploads"
    SESSION_COOKIE_SECURE = True
    
    # The absolute path of the directory containing images for users to download
    CLIENT_IMAGES = PureWindowsPath("C:/Users/pusch/Documents/python/website/app/static/client/img")

    # The absolute path of the directory containing CSV files for users to download
    CLIENT_CSV = PureWindowsPath("C:/Users/pusch/Documents/python/website/app/static/client/csv")

    # The absolute path of the directory containing PDF files for users to download
    CLIENT_PDF = PureWindowsPath("C:/Users/pusch/Documents/python/website/app/static/client/pdf")
    
class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    
    IMAGE_UPLOADS = "/home/username/projects/my_app/app/static/images/uploads"
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True
    
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    
    SESSION_COOKIE_SECURE = False