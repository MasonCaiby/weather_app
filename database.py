# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
import json
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

def grab_data():
    with open('config.json', 'r') as infile:
        data = json.load(infile)

    DATABASE_URI = f"postgres+psycopg2://postgres:{data['password']}@localhost:{data['port']}/{data['server_name']}"

    return data, DATABASE_URI

def create_database():
    con = psycopg2.connect(dbname='postgres',
                           user=data['user'], host='',
                           password=data['password'])
    con.autocommit = True
    cur = con.cursor()
    try:
        cur.execute(f""" CREATE DATABASE weather_app
                        WITH 
                        OWNER = {data['user']}
                        ENCODING = 'UTF8'
                        CONNECTION LIMIT = -1;"""
                )
    except psycopg2.errors.DuplicateDatabase:
        print('Duplicate Database, passing')

class Recipient(declarative_base()):
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    city = Column(String)
    name = Column(String)
    data, DATABASE_URI = grab_data()

    def __repr__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email,
                                                                self.city,
                                                                self.name)

    def __str__(self):
        return "<User(email='{}', city='{}', name='{}'>".format(self.email,
                                                                self.city,
                                                                self.name)

def get_session():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    return engine, Session

def add_email(Session, email, location, name=None):
    session = Session()
    recipient = Recipient(email = email,
                          location = location,
                          name = name
                          )
    session.add(recipient)
    session.commit()
    session.close()

if __name__ == "__main__":
    data, DATABASE_URI = grab_data()
    create_database()
