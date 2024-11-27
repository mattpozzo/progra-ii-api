import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:M1croCuts@127.0.0.1:5432/progra-ii"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "hola1234"
