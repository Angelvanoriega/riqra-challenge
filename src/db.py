#!/usr/bin/python
import psycopg2
from src.config_db import config


class DataBase(object):
    cursor = None
    connection = None

    def __init__(self):
        params = config()
        self.connection = psycopg2.connect(**params)
        self.cursor = self.connection.cursor()
