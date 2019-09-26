# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
import json
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

class Database:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.data = None
        self.DATABASE_URI = None
        self.engine = None
        self.Session = None

        self.grab_data()
        self.get_session()

    def grab_data(self):
        with open('config.json', 'r') as infile:
            self.data = json.load(infile)

        self.DATABASE_URI = f"postgres+psycopg2://postgres:{self.data['database_password']}"+\
                       f"@localhost:{self.data['port']}/{self.data['server_name']}"

    def get_session(self):
        self.engine = create_engine(self.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self):
        con = psycopg2.connect(user=self.data['database_user'], host='',
                               password=self.data['database_password'])
        con.autocommit = True
        cur = con.cursor()

        try:
            cur.execute(f""" CREATE DATABASE weather_app
                             WITH 
                             OWNER = {self.data['database_user']}
                             ENCODING = 'UTF8'
                             CONNECTION LIMIT = -1;"""
                        )

        except psycopg2.errors.DuplicateDatabase:
            print('Duplicate Database, passing')

    def create_table(self):
        con = psycopg2.connect(dbname='weather_app',
                               user=self.data['database_user'],
                               host='',
                               password=self.data['database_password'])
        con.autocommit = True
        cur = con.cursor()

        try:
            cur.execute("""CREATE TABLE recipients(
                           id serial PRIMARY KEY,
                           email TEXT UNIQUE,
                           city TEXT,
                           name TEXT
                           );""")
        except psycopg2.errors.DuplicateTable:
            print('Duplicate Table, passing')

    def add_email(self, email, location, name=''):
        session = self.Session()
        recipient = Recipient(email=email,
                              city=location,
                              name=name
                              )
        session.add(recipient)
        session.commit()
        session.close()

class Recipient(declarative_base()):

    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    city = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email,
                                                                self.city,
                                                                self.name)

    def __str__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email,
                                                                self.city,
                                                                self.name)

if __name__ == "__main__":
    database = Database('config.json')
    database.create_database()
    database.create_table()