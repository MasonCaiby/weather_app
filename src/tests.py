import unittest, json
import sqlalchemy, psycopg2

from database import Database
from app import add_to_database

database = Database()


class TestDB(unittest.TestCase):

    def test_make_db(self):
        database.create_database(dbname='weather_app',
                                 user=database.data['database_user'],
                                 password=database.data['database_password'])

    def test_make_table(self):
        database.create_table(dbname='weather_app',
                              user=database.data['database_user'],
                              password=database.data['database_password'],
                              table_name='recipients')

    def test_tearDown(self):
        self.connection.execute("DROP DATABASE testdb")


class TestInputs(unittest.TestCase):

    def test_valid_data(self):
        email = "fake_test@fake_test.com"
        city = "Richmond, Virginia"

        database.delete_email(email)

        test_string = f'<SCRIPT>alert("User {email} added with City {city}")</SCRIPT>'

        self.assertEqual(add_to_database(database, email, city), test_string)

    def test_invalid_email(self):
        email = "te/st@test.com"
        city = "Richmond, Virginia"

        test_string = '<SCRIPT>alert("Please enter a valid email and City.")</SCRIPT>'

        self.assertEqual(add_to_database(database, email, city), test_string)

    def test_existing_user(self):
        email = "test@test.com"
        city = "Richmond, Virginia"

        test_string = f'<SCRIPT>alert("User {email} Already Exists.")</SCRIPT>'
        add_to_database(database, email, city)

        self.assertEqual(add_to_database(database, email, city), test_string)

    def test_not_enough_data(self):
        pass


if __name__ == '__main__':
    unittest.main()