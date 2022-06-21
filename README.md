# HabitBackend
A python habit tracker created as a project for the course: Object Oriented and Functional Programming with Python.

This habit tracker lets you create daily and weekly specified habits.
A basic CLI is used to operate the program.

Each habit needs to be checked-off at least once during the defined period (daily or wekkly). If you miss to check a habit during this period you are said to break the habit.
When you check a habit, the period will restart from this point on. Both periods only count in days, so the time on a specific day does not matter for calculating a streak.

Installation process:
Please install Python from the official website:
https://www.python.org/downloads/
It provides a well written guide for installation and usage: https://wiki.python.org/moin/BeginnersGuide
Unzip the file and execute the Run.py

Five habits are predefined with name, specification and period:
Teeth - Brush your teeth every day - daily
Garbage - Bring out the garbage every week - weekly
Bathroom - Clean the bathroom every week - weekly
Pets - Feed the pets every day - daily
Training - Perform a little workout every day - daily

Upon startup you will receive an overview about your tracked habits. In every main screen you can acces the user instructions by typing help. 
You will start at the HOME screen and return there every time you complete a operation in the program.
To switch screens just type the name of the screen you want to visit:
CHECK - When you completed a task type in CHECK to let the program know.
EDIT - the edit screen provides the possibility to create or delete a habit as well as view a list of all habits.
ANALYTIC - the analytic screen provides the possibility to return the streak of a given habit, return a list of all habits, return all daily or all weekly habits, return your maximum streak or the habit you have the most trouble to complete. You can also view all data of a specific habit.
PULL - Gives an overwiev about your habits, you get the name, the streaklist (the individual streaks of a habit) and the highest streak
Each screen is a step to a specific option. After every option you will be guided back to home screen.
To terminate the program type EXIT.

EDIT screen:
In this screen you can CREATE and DELETE habits. For a better overview you can also LIST all habits here.

You can perform the following actions:
LIST - Shows you a list of all habits to get the ID for the other functions.
CREATE - Lets you create a new habit.
DELETE - Lets you delete a habit. all information will be lost.
Type HOME to switch back to the Home screen.
After every action, you will be back at the home screen.

ANALYTIC screen:
In this screen you can analyse your habits and access all gathered information.

You can call the following functions:
LIST - Shows you a list of all habits to get the ID for the other functions.
DAILY - Shows you a list of all habits with the period daily.
WEEKLY - Shows you a list of all habits with the period weekly.
HABIT - Shows you ID, Name, Description, Period and Creation Date of a habit.
STREAK - Shows you the streak of a given habit.
LONGEST - Shows you the habit with the longest streak
TROUBLE - Shows you the habit with the most breaks
Type HOME to switch back to the Home screen.
After every action, you will be back at the home screen.

The software provides a testing environment utilizing pytest.


Please note:
The tracker is written in Python 3.9
All dates are calculated utilizing the GMT.
