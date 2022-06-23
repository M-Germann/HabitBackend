#!/usr/bin/python
"""Make the code able to run in a unix environment"""

"""Database contains all functions of the Database Layer"""

"""Load necessary modules"""
import sqlite3      #Link to SQL Database
import os.path      #Check for Database

"""Link to necessary scripts"""
from Objects import *

class Database:
    """Create a habit database or connect to it if it already exists."""
    def create_database(self):
        if os.path.isfile('habit_db.sqlite'):
            self.conn = sqlite3.connect('habit_db.sqlite')  #Connect to database
            print('Database found')
        else:
            """Create database"""
            self.conn = sqlite3.connect('habit_db.sqlite')
            """Create a cursor to execute SQL code"""
            cur = self.conn.cursor()
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
            """Save change to database"""
            self.conn.commit()
            '''If the database is new, the five predifined habits have to be created '''
            temp_habit=Habit('Teeth', 'Brush your teeth every day', 'daily')
            self.create_habit(temp_habit)
            temp_habit=Habit('Garbage', 'Bring out the garbage every week', 'weekly')
            self.create_habit(temp_habit)
            temp_habit=Habit('Bathroom', 'Clean the bathroom every week', 'weekly')
            self.create_habit(temp_habit)
            temp_habit=Habit('Pets', 'Feed the pets every day', 'daily')
            self.create_habit(temp_habit)
            temp_habit=Habit('Training', 'Perform a little workout every day', 'daily')
            self.create_habit(temp_habit)
            self.conn.commit()  # Save changes
            print('Database created')

    def create_habit(self, habit):
        cur = self.conn.cursor()
        """Insert habit data to database"""
        cur.execute('INSERT INTO habits (name, specification, period) VALUES (?, ?, ?)',
                    (habit.name, habit.spec, habit.period))
        self.conn.commit()  # Save changes

    def delete_habit(self):
        '''Deletes Habit data from the database'''
        id = input('Enter habit ID to be deleted:')
        cur = self.conn.cursor()
        cur.execute('SELECT name FROM habits WHERE id=?', (id,))
        name = cur.fetchone()[0]
        command = input('You want to delete habit ' + str(name) + '. Please type YES to confirm.').upper()
        if command == 'YES':
            cur.execute('DELETE FROM habits WHERE id=?', (id,))
            self.conn.commit()  # Save changes
            print('Habit ' + str(id) + ' ' + str(name) + ' deleted.')
        else:
            print('Deleting habit cancelled.')

    def query_tracked(self):  # Returns a list of all tracked habits
        '''Pulls a list of all habits from the database and print every row as a line'''
        cur = self.conn.cursor()
        cur.execute('SELECT id, name, specification, period FROM habits')
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def pull_habits(self):
        '''Pull all habit information as instance of a class for the processing layer '''
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM habits')
        habits = cur.fetchall()
        result = []
        for habit in habits:
            temp_habit = Habit(habit[1], habit[2], habit[3], habit[0], habit[4])
            result.append(temp_habit)
        return result

    def pull_checks(self):
        '''Pull all check information as instance of a class for the processing layer '''
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM habit_checks')
        checks = cur.fetchall()
        result = []
        for check in checks:
            temp_check = Check(check[0], check[1], check[2])
            result.append(temp_check)
        return result

    def check_habit(self):
        '''Creates a check entry in the database supported by a simple CLI'''
        id = input('Please type in the number of the habit you want to check:')
        cur = self.conn.cursor()
        cur.execute('SELECT name FROM habits WHERE id=?', (id,))
        name = cur.fetchone()[0]
        command = input('You want to check habit ' + str(name) + '. Please type YES to confirm.').upper()
        if command == 'YES':
            cur = self.conn.cursor()
            """Insert data to database"""
            cur.execute('INSERT INTO habit_checks (habit_id) VALUES (?)', (id,))
            self.conn.commit()  # Save changes
            print('Habit ' + str(id) + ' ' + str(name) + ' checked.')
        else:
            print('Habit check cancelled.')

    def return_habit(self, id):  # Return a habit with all information
        '''Prints all information about a habit as a row'''
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM habits WHERE id=?', (id,))
        name = cur.fetchall()
        for row in name:
            print("Id: ", row[0])
            print("Habit: ", row[1])
            print("Specification: ", row[2])
            print("Period: ", row[3])
            print("Creation: ", row[4])
            print("\n")

    def return_daily(self):  # Return list of all tracked daily habits
        '''Pulls all names from the daily habits and print them as list'''
        cur = self.conn.cursor()
        period = 'daily'
        cur.execute('SELECT name FROM habits WHERE period=?', (period,))
        name = cur.fetchall()
        print('Here are your daily habits: ' + str(name))

    def return_weekly(self):  # Return list of all tracked weekly habits
        '''Pulls all names from the weekly habits and print them as list'''
        cur = self.conn.cursor()
        period = 'weekly'
        cur.execute('SELECT name FROM habits WHERE period=?', (period,))
        name = cur.fetchall()
        print('Here are your weekly habits: ' + str(name))

    def close_database(self):
        '''Closes database when tracker shuts down to prevent errors'''
        self.conn.close()