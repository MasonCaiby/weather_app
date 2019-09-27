""" Just the main file for the CLI"""

import argparse
import os, sys
sys.path.append(os.path.dirname(__file__))

from database import Database
from weather_api import email_blast

def main():
    parser = argparse.ArgumentParser(
        description="Send a custom email to all registered email addresses in the database")

    database = Database()
    email_blast(database)


if __name__ == '__main__':
    main()
