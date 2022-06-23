'''Testing functions of the Database module'''
import pytest
import os.path      #Check for Database
import datetime     #Calculate testing data
from Database import *

database=Database()
''' The first tests creates a database if not already existent, then checks if the right tables are present. Then create_habit is executed for the predefined habits and assured the right data fills the tables. The creation date is set 4 weeks in the past to match testing data.'''
def test_create_database():                     # Tests create_database, create_habit and query_tracked
    if os.path.isfile('habit_db.sqlite'):
        conn = sqlite3.connect('habit_db.sqlite')  # Connect to database
        print('Database found')
    else:
        """Create database"""
        conn = sqlite3.connect('habit_db.sqlite')
        """Create a cursor to execute SQL code"""
        cur = conn.cursor()
        """Create table"""
        sql_command = """
        CREATE TABLE habits (
        id INTEGER,
        name VARCHAR,
        specification VARCHAR,
        period VARCHAR,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id));
        """
        cur.executescript(sql_command)
        sql_command = """
        CREATE TABLE habit_checks (
        id INTEGER,
        habit_id INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(id));
        """
        cur.executescript(sql_command)
        '''If the database is new, the five predifined habits have to be created '''
        database.conn = sqlite3.connect('habit_db.sqlite')
        cur = database.conn.cursor()
        temp_habit = Habit('Teeth', 'Brush your teeth every day', 'daily')
        database.create_habit(temp_habit)
        temp_habit = Habit('Garbage', 'Bring out the garbage every week', 'weekly')
        database.create_habit(temp_habit)
        temp_habit = Habit('Bathroom', 'Clean the bathroom every week', 'weekly')
        database.create_habit(temp_habit)
        temp_habit = Habit('Pets', 'Feed the pets every day', 'daily')
        database.create_habit(temp_habit)
        temp_habit = Habit('Training', 'Perform a little workout every day', 'daily')
        database.create_habit(temp_habit)
        '''To fit the four weeks of testing data, the creation date of the predefined habits must be set 4 weeks in 
        the past. Created at has to be checked immediately because calculated time will change every second.'''
        daydelta = datetime.datetime.now() - datetime.timedelta(days=28)
        day = daydelta.replace(microsecond=0)
        cur.execute('UPDATE habits SET created_at = (?) WHERE id = 1',
                    (day, ))
        cur.execute('SELECT created_at FROM habits WHERE id=1')
        name = str(cur.fetchone())
        assert name == ("('" + str(day) + "',)")
        cur.execute('UPDATE habits SET created_at = (?) WHERE id = 2',
                    (day, ))
        cur.execute('SELECT created_at FROM habits WHERE id=2')
        name = str(cur.fetchone())
        assert name == ("('" + str(day) + "',)")
        cur.execute('UPDATE habits SET created_at = (?) WHERE id = 3',
                    (day, ))
        cur.execute('SELECT created_at FROM habits WHERE id=3')
        name = str(cur.fetchone())
        assert name == ("('" + str(day) + "',)")
        cur.execute('UPDATE habits SET created_at = (?) WHERE id = 4',
                    (day, ))
        cur.execute('SELECT created_at FROM habits WHERE id=4')
        name = str(cur.fetchone())
        assert name == ("('" + str(day) + "',)")
        cur.execute('UPDATE habits SET created_at = (?) WHERE id = 5',
                    (day, ))
        cur.execute('SELECT created_at FROM habits WHERE id=5')
        name = str(cur.fetchone())
        assert name == ("('" + str(day) + "',)")
        conn.commit()  # Save changes
        print('Database created')
    '''Check for database file'''
    assert os.path.isfile('habit_db.sqlite')
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=str(cur.fetchall())
    '''Chck tables'''
    assert tables == ("[('habits',), ('habit_checks',)]")
    '''Check Habit 1'''
    cur.execute('SELECT * FROM habits WHERE id=1')
    name = cur.fetchall()
    for row in name:
        assert row[0] == 1
        assert row[1] == 'Teeth'
        assert row[2] == 'Brush your teeth every day'
        assert row[3] == 'daily'
    '''Check Habit 2'''
    cur.execute('SELECT * FROM habits WHERE id=2')
    name = cur.fetchall()
    for row in name:
        assert row[0] == 2
        assert row[1] == 'Garbage'
        assert row[2] == 'Bring out the garbage every week'
        assert row[3] == 'weekly'
    '''Check Habit 3'''
    cur.execute('SELECT * FROM habits WHERE id=3')
    name = cur.fetchall()
    for row in name:
        assert row[0] == 3
        assert row[1] == 'Bathroom'
        assert row[2] == 'Clean the bathroom every week'
        assert row[3] == 'weekly'
    '''Check Habit 4'''
    cur.execute('SELECT * FROM habits WHERE id=4')
    name = cur.fetchall()
    for row in name:
        assert row[0] == 4
        assert row[1] == 'Pets'
        assert row[2] == 'Feed the pets every day'
        assert row[3] == 'daily'
    '''Check Habit 5'''
    cur.execute('SELECT * FROM habits WHERE id=5')
    name = cur.fetchall()
    for row in name:
        assert row[0] == 5
        assert row[1] == 'Training'
        assert row[2] == 'Perform a little workout every day'
        assert row[3] == 'daily'
    database.close_database()

def calculate_testing_data(id, daynum):             #If further tests pass, check_habit works as well.
    '''function to calculate a testing check entry'''
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    daydelta = datetime.datetime.now() - datetime.timedelta(days=daynum)
    day = daydelta.replace(microsecond=0)
    cur.execute('INSERT INTO habit_checks (habit_id, created_at) VALUES (?, ?)',
                (id, day))
    conn.commit()  # Save changes
    database.close_database()

def test_create_testing_data():
    '''Creating 4 weeks of test data'''
    '''4 Weeks of testing data will be created to run the system tests. First integer is habit_id, second one is days in the past'''
    '''Habit one describes the case a habit streak is unbroken and still ongoing.'''
    calculate_testing_data(1, 28)
    calculate_testing_data(1, 27)
    calculate_testing_data(1, 26)
    calculate_testing_data(1, 25)
    calculate_testing_data(1, 24)
    calculate_testing_data(1, 23)
    calculate_testing_data(1, 22)
    calculate_testing_data(1, 21)
    calculate_testing_data(1, 20)
    calculate_testing_data(1, 19)
    calculate_testing_data(1, 18)
    calculate_testing_data(1, 17)
    calculate_testing_data(1, 16)
    calculate_testing_data(1, 15)
    calculate_testing_data(1, 14)
    calculate_testing_data(1, 13)
    calculate_testing_data(1, 12)
    calculate_testing_data(1, 11)
    calculate_testing_data(1, 10)
    calculate_testing_data(1, 9)
    calculate_testing_data(1, 8)
    calculate_testing_data(1, 7)
    calculate_testing_data(1, 6)
    calculate_testing_data(1, 5)
    calculate_testing_data(1, 4)
    calculate_testing_data(1, 3)
    calculate_testing_data(1, 2)
    calculate_testing_data(1, 1)
    '''Habit two describes the case a habit streak is broken once but still ongoing.'''
    calculate_testing_data(2, 27)
    calculate_testing_data(2, 20)
    calculate_testing_data(2, 13)
    calculate_testing_data(2, 6)
    '''Habit three describes the case a habit streak was maintained but is now broken and not ongoing.'''
    calculate_testing_data(3, 28)
    calculate_testing_data(3, 21)
    calculate_testing_data(3, 15)
    calculate_testing_data(3, 9)
    '''Habit four describes a case of an often struggeled habit but now maintained. Highest streak 10, 4 breaks, streak ongoing.'''
    calculate_testing_data(4, 28)
    calculate_testing_data(4, 27)
    calculate_testing_data(4, 26)
    calculate_testing_data(4, 25)
    calculate_testing_data(4, 24)
    calculate_testing_data(4, 23)
    calculate_testing_data(4, 22)
    calculate_testing_data(4, 21)
    calculate_testing_data(4, 20)
    calculate_testing_data(4, 19)
    calculate_testing_data(4, 18)
    calculate_testing_data(4, 16)
    calculate_testing_data(4, 15)
    calculate_testing_data(4, 14)
    calculate_testing_data(4, 12)
    calculate_testing_data(4, 11)
    calculate_testing_data(4, 10)
    calculate_testing_data(4, 8)
    calculate_testing_data(4, 7)
    calculate_testing_data(4, 6)
    calculate_testing_data(4, 4)
    calculate_testing_data(4, 3)
    calculate_testing_data(4, 2)
    calculate_testing_data(4, 1)
    '''Habit five has no streak at all, but the most trouble.'''
    calculate_testing_data(5, 28)
    calculate_testing_data(5, 26)
    calculate_testing_data(5, 24)
    calculate_testing_data(5, 22)
    calculate_testing_data(5, 20)
    calculate_testing_data(5, 18)
    calculate_testing_data(5, 16)
    calculate_testing_data(5, 14)
    calculate_testing_data(5, 12)
    calculate_testing_data(5, 10)
    calculate_testing_data(5, 8)
    calculate_testing_data(5, 6)
    calculate_testing_data(5, 4)
    calculate_testing_data(5, 2)

def test_return_daily():                        # Tests return_daily
    '''Pulls all names from the daily habits and print them as list'''
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    period = 'daily'
    cur.execute('SELECT name FROM habits WHERE period=?', (period,))
    name = cur.fetchall()
    assert str(name) == "[('Teeth',), ('Pets',), ('Training',)]"
    database.close_database()

def test_return_weekly():                       # Tests return_weekly
    '''Pulls all names from the weekly habits and print them as list'''
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    period = 'weekly'
    cur.execute('SELECT name FROM habits WHERE period=?', (period,))
    name = cur.fetchall()
    assert str(name) == "[('Garbage',), ('Bathroom',)]"
    database.close_database()