import os
import json
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database:
    """ A class to handle all interactions with a Database. It takes an optional config_file location,
        in case you want to save your config elsewhere."""

    def __init__(self, config_file=os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')):
        self.config_file = config_file

        self.grab_data()
        self.get_session()

    def grab_data(self):
        """ Grabs the data from the config file and also makes a DATABSE_URI. I believe psycopg2 convention is
            to have that variable name in all caps."""
        with open(self.config_file, 'r') as infile:
            self.data = json.load(infile)

        # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
        self.DATABASE_URI = f"postgres+psycopg2://postgres:{self.data['database_password']}"+\
                            f"@localhost:{self.data['port']}/{self.data['server_name']}"

    def get_session(self):
        """ This safely makes a sqlalchemy connection engine and a Session instance. The Session isn't fully formed,
            so we can keep making new ones off the same instance."""
        self.engine = create_engine(self.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self):
        """ This will make a new database, to help with setup."""

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
        """ This safely makes the DB's only table, called weather_app. It takes an optional name parameter, in case we
            want to further customize the emails later."""

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
        """ Adds an email to the data base."""

        session = self.Session()
        recipient = Recipient(email=email,
                              city=location,
                              name=name)

        session.add(recipient)
        session.commit()
        session.close()


class Recipient(declarative_base()):
    """ A class so we can add email recipients to the database."""
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    city = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email, self.city, self.name)

    def __str__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email, self.city, self.name)


if __name__ == "__main__":
    database = Database()
    database.create_database()
    database.create_table()
