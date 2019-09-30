import unittest, json
import sqlalchemy, psycopg2

from database import Database
from app import add_to_database
from weather_api import make_subject

database = Database()


class TestDB(unittest.TestCase):

    def test_make_db(self):
        database.create_database(dbname='weather_app')

    def test_make_and_delete_table(self):
        database.create_table(dbname='weather_app',
                              table_name='testdb')

        con = psycopg2.connect(dbname='weather_app',
                               user=database.data['database_user'],
                               host='',
                               password=database.data['database_password'])
        con.autocommit = True
        cur = con.cursor()
        cur.execute("DROP TABLE testdb")


class TestInputs(unittest.TestCase):

    def test_valid_data(self):
        email = "fake_test@fake_test.com"
        city = "Richmond, Virginia"

        database.delete_email(email)

        test_string = f'<SCRIPT>alert("User {email} added with City {city}")</SCRIPT>'

        self.assertEqual(add_to_database(email, city), test_string)

    def test_invalid_email(self):
        email = "te/st@test.com"
        city = "Richmond, Virginia"

        test_string = '<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>'

        self.assertEqual(add_to_database(email, city), test_string)

    def test_existing_user(self):
        email = "test@test.com"
        city = "Richmond, Virginia"

        test_string = f'<SCRIPT>alert("User {email} Already Exists.")</SCRIPT>'
        add_to_database(email, city)

        self.assertEqual(add_to_database(email, city), test_string)

    def test_not_enough_data(self):
        test_string = '<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>'
        self.assertEqual(add_to_database('', "Richmond, Virginia"), test_string)
        self.assertEqual(add_to_database("test@test.com", None), test_string)


class TestEmail(unittest.TestCase):
    def test_nice_temp(self):
        self.assertEqual(make_subject(current_temp=70, tomorrow_temp=65, current_code=201),
                         "It's nice out! Enjoy a discount on us.")

    def test_sunny(self):
        self.assertEqual(make_subject(current_temp=70, tomorrow_temp=70, current_code=800),
                         "It's nice out! Enjoy a discount on us.")

    def test_raining(self):
        self.assertEqual(make_subject(current_temp=70, tomorrow_temp=70, current_code=201),
                         "Not so nice out? That's okay, enjoy a discount on us.")

    def test_not_nice_temp(self):
        self.assertEqual(make_subject(current_temp=70, tomorrow_temp=75, current_code=802),
                         "Not so nice out? That's okay, enjoy a discount on us.")

    def test_normal_weather(self):
        self.assertEqual(make_subject(current_temp=70, tomorrow_temp=72, current_code=802),
                         "Enjoy a discount on us.")

if __name__ == '__main__':
    unittest.main()