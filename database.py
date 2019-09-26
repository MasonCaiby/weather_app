# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
import json
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


def grab_data():
    with open('config.json', 'r') as infile:
        data = json.load(infile)

    DATABASE_URI = f"postgres+psycopg2://postgres:{data['database_password']}@localhost:{data['port']}/{data['server_name']}"

    return data, DATABASE_URI


def create_database():
    con = psycopg2.connect(user=data['database_user'], host='',
                           password=data['database_password'])
    con.autocommit = True
    cur = con.cursor()

    try:
        cur.execute(f""" CREATE DATABASE weather_app
                        WITH 
                        OWNER = {data['database_user']}
                        ENCODING = 'UTF8'
                        CONNECTION LIMIT = -1;"""
                    )

    except psycopg2.errors.DuplicateDatabase:
        print('Duplicate Database, passing')


def create_table():
    con = psycopg2.connect(dbname='weather_app',
                           user=data['database_user'],
                           host='',
                           password=data['database_password'])
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


def get_session(DATABASE_URI):
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    return engine, Session


def add_email(Session, email, location, name=''):
    session = Session()
    recipient = Recipient(email=email,
                          city=location,
                          name=name
                          )
    session.add(recipient)
    session.commit()
    session.close()

if __name__ == "__main__":
    data, DATABASE_URI = grab_data()
    create_database()
    create_table()
