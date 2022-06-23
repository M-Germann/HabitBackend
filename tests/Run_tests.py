#!/usr/bin/python
"""Make the code able to run in a unix environment"""
from tests.test_Analytic import *
from tests.test_Database import *
import os.path      #Used to delete database at the end.

"""Run contains all functions to execute and operate the program"""
if os.path.isfile('habit_db.sqlite'):
    os.remove("habit_db.sqlite")
else:
    pass
test_create_database()
print('Database for testing created.')
print('Functions create_database, create_habit and query_tracked functional.')
test_create_testing_data()
print ('4 weeks of dummy data created for testing.')
test_return_daily()
print('Function test_return_daily() functional.')
test_return_weekly()
print('Function test_return_weekly() functional.')
print('All database operations functional.')
test_return_pending()
test_return_streak()
test_return_max_streak()
test_return_max_break()
print('All analytic functions functional')
print('')
print('Program functional.')
process = input('If you want to keep the testing database to copy it in the main folder please type KEEP. Otherwise just hit Enter.').upper()
if process == "KEEP":
    os.remove("habit_db.sqlite")
    print('Database for testing removed.')
else:
    pass
print('Database kept for user. Next testing will delete it.')
