#!/usr/bin/python
"""Make the code able to run in a unix environment"""

"""Core contains all functions of the CLI-Layer including all user interaction methods"""

"""Link to necessary scripts"""
from Database import *
from Analytic import *


class Core:
    '''This class holds the CLI created by a simple flow of Input requests and print commands. Check the user interaction diagram for a better overview.'''
    def run_program(self):          # Initial run
        '''Create objects for the analytic and database class to operate the corresponding methods.'''
        self.analytic=Analytic()
        self.database=Database()
        '''Übergebe database Objekt an Analytic. +++Später nochmal in schön+++'''
        self.analytic.database=self.database
        '''This method is used to start the tracker and shut it down.'''
        try:
            self.database.create_database()
            self.database.pull_habits()
            self.database.pull_checks()
            self.show_home()
        finally:                # Stops the program
            self.database.close_database()
            print('Tracker shutdown')  # Indicates the progrum shuts down properly

    def show_home(self):            # Return home screen
        '''The CLI for the Home Screen'''
        print('+++ HOME +++')
        print('Welcome to your habit tracker, from this screen you can access the functions of this tracker:')
        print(' ')
        self.analytic.calculate_streaks()
        self.analytic.return_pending()
        print(' ')
        command='empty'
        tracker_on = True
        while tracker_on == True:
            print('+++HOME+++')
            print('You are on home screen.')
            print('You can CHECK a habit when you concluded the task. You can also switch to EDIT or ANALYTIC screens.')
            print('To get a habit overview type PULL.')
            print('Type EXIT to close the program.')
            print('If you need assistance please type HELP.')
            command = input('Where do you want to go?').upper()
            if command == 'CHECK':
                self.database.check_habit()
            elif command == 'EDIT':
                self.show_edit()
            elif command == 'ANALYTIC':
                self.show_analytic()
            elif command == 'PULL':
                self.analytic.calculate_streaks()
                self.analytic.return_pending()
            elif command == 'EXIT':
                tracker_on = False
            elif command == 'HELP':
                self.help_home()
            elif command == 'TEST':
                self.database.create_testing_data()
            else:
                print('Invalid entry. Please type CHECK, EDIT, ANALYTIC or HELP to proceed.')


    def show_analytic(self):        # Return analytic screen
        '''The CLI for the Analytic Screen'''
        print('+++ANALYTIC+++')
        print('This screen provides the possibility to view all data of a chosen HABIT, the STREAK of a chosen habit, a LIST of all tracked habits, a list of all DAILY or WEEKLY habits, the habit with the LONGEST streak or the habit with the most TROUBLE. If you need assistance please type HELP.')
        print('Type HOME to get back to home screen')
        command = 'empty'
        #while command != 'HABIT' or command != 'STREAK' or command != 'LIST' or command != 'DAILY' or command != 'WEEKLY' or command != 'LONGEST' or command != 'TROUBLE' or command != 'HOME' or command != 'HELP':
        command = input('What do you want to view?').upper()
        if command == 'HABIT':
            id = input('Please type in the number of the habit you want to see:')
            self.database.return_habit(id)
        elif command == 'STREAK':
            self.analytic.return_streak()
        elif command == 'LIST':
            print("Here are your habits showed with name, description and period:")
            self.database.query_tracked()
        elif command == 'DAILY':
            self.database.return_daily()
        elif command == 'WEEKLY':
            self.database.return_weekly()
        elif command == 'LONGEST':
            self.analytic.return_max_streak()
        elif command == 'TROUBLE':
            self.analytic.return_max_break()
        elif command == 'HELP':
            self.help_analytic()
        else:
            print('Invalid entry. Please type HABIT, STREAK, LIST, DAILY, WEEKLY, LONGEST, TROUBLE, or HELP to proceed in ANALYTIC. Type HOME to go back to home screen.')

    def show_edit(self):            # Return edit screen
        '''The CLI for the Edit Screen'''
        print('+++EDIT+++')
        print('This screen provides the possibility to CREATE and DELETE a habit. You can also LIST all tracked habits. If you need assistance please type HELP.')
        print('Type HOME to get back to home screen')
        command = 'empty'
        command = input('What do you want to do?').upper()
        if command == 'CREATE':                 #Creation of a habit
            period = 'empty'
            name = input('Please choose a name for your habit.')
            spec = input('Please describe the habit in a short sentence.')
            period = input('Do you want to create a Daily or a Weekly habit? Type STOP to cancel the habit creation. Please type DAILY, WEEKLY or STOP to proceed.').upper()
            if period == 'DAILY':
                period = 'daily'
                temp_habit = Habit(str(name), str(spec), str(period))
                self.database.create_habit(temp_habit)
                print('Daily habit ' + str(name) + ' created.')
            elif period == 'WEEKLY':
                period = 'weekly'
                temp_habit = Habit(str(name), str(spec), str(period))
                self.database.create_habit(temp_habit)
                print('Weekly habit ' + str(name) + ' created.')
            elif period == 'STOP':
                print('Creation canceled. Going back to HOME.')
            else:
                print('Invalid entry. Please type Daily, Weekly or STOP to proceed.')
        elif command == 'DELETE':
            self.database.delete_habit()
        elif command == 'LIST':
            print("Here are your habits showed with name, description and period:")
            self.database.query_tracked()
        elif command == 'HOME':
            self.show_home()
        elif command == 'HELP':
            self.help_edit()
        else:
            print('Invalid entry. Please type CREATE, DELETE, LIST, HOME or HELP to proceed in EDIT.')

    '''All Help Screens are hold here. It's a simple print output of all possible functions in the screen they belong to.'''
    def help_home(self):            # Return user interaction possibilities in home screen
        print('Each habit needs to be checked-off at least once during the defined period (daily or wekkly). If you miss to check a habit during this period you are said to break the habit.')
        print('When you check a habit, the period will restart from this point on. Both periods only count in days, so the time on a specific day does not matter for calculating a streak.')
        print('')
        print('To switch screens just type the name of the screen you want to visit:')
        print('CHECK - When you completed a task type in CHECK to let the program know.')
        print('EDIT - the edit screen provides the possibility to create or delete a habit as well as view a list of all habits.')
        print('ANALYTIC - the analytic screen provides the possibility to return the streak of a given habit, return a list of all habits, return all daily or all weekly habits, return your maximum streak or the habit you have the most trouble to complete. You can also view all data of a specific habit.')
        print('PULL - Gives an overwiev about your habits, you get the name, the streaklist (the individual streaks of a habit) and the highest streak')
        print('Each screen is a step to a specific option. After every option you will be guided back to home screen.')
        print('')
        print('To terminate the program type EXIT.')

    def help_analytic(self):  # Return user interaction possibilities in analytic screen
        print('In this screen you can analyse your habits and access all gathered information.')
        print('')
        print('You can call the following functions:')
        print('LIST - Shows you a list of all habits to get the ID for the other functions.')
        print('DAILY - Shows you a list of all habits with the period daily.')
        print('WEEKLY - Shows you a list of all habits with the period weekly.')
        print('HABIT - Shows you ID, Name, Description, Period and Creation Date of a habit.')
        print('STREAK - Shows you the streak of a given habit.')
        print('LONGEST - Shows you the habit with the longest streak')
        print('TROUBLE - Shows you the habit with the most breaks')
        print('Type HOME to switch back to the Home screen.')
        print('After every action, you will be back at the home screen.')

    def help_edit(self):  # Return user interaction possibilities in edit screen
        print('In this screen you can CREATE and DELETE habits. For a better overview you can also LIST all habits here.')
        print('')
        print('You can perform the following actions:')
        print('LIST - Shows you a list of all habits to get the ID for the other functions.')
        print('CREATE - Lets you create a new habit.')
        print('DELETE - Lets you delete a habit. all information will be lost.')
        print('Type HOME to switch back to the Home screen.')
        print('After every action, you will be back at the home screen.')