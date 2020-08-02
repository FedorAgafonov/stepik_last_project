import os

db_path = "sqlite:///test.db"


class Config:
    DEBUG = False
    SECRET_KEY = "lviybaysv"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
