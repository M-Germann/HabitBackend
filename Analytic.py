#!/usr/bin/python
"""Make the code able to run in a unix environment"""

"""Analytic contains all functions of the Analytic Layer to process information from the database"""

"""Load necessary modules"""
import datetime     #calculate with dates

"""Link to necessary scripts"""
from Database import *

class Analytic:
    '''Pulls habits and checks as instances of their classes from the database and then sorts the checks to their respective habits'''
    def sort_data(self):
        habits = self.database.pull_habits()
        checks = self.database.pull_checks()
        for habit in habits:
            for check in checks:
                if check.habit_id == habit.id:
                    habit.habit_checks.append(check)
        return habits

    def calculate_streaks(self, mode="", printit=""):
        '''For ecery habit check this takes a check as first date, calculates the maximum timepoint for the next check according to the period delta as temp_date and compares it to actual next check second_date'''
        '''If the streak is maintained, the streak counter in streaklist will increase by one. If not, a new 0 will be appended to the list. So the current and highest streak are calculated and the length of the list -1 is the number of breaks.'''
        habits = self.sort_data()
        maxstreak = -1
        maxstreak_habitname = ""
        maxbreak = -1
        maxbreak_habitname = ""
        for habit in habits:
            if habit.period == "daily":
                delta = 1
            if habit.period == "weekly":
                delta = 7
            streaklist = [0]
            for i in range(len(habit.habit_checks)-1):
                first_date = datetime.datetime.strptime(str(habit.habit_checks[i].created_at).split()[0], '%Y-%m-%d')
                second_date = datetime.datetime.strptime(str(habit.habit_checks[i+1].created_at).split()[0], '%Y-%m-%d')
                temp_date = first_date + datetime.timedelta(days=delta)
                if temp_date >= second_date:
                    streaklist[-1] += 1
                else:
                    streaklist.append(0)
            habit.highest_streak = max(streaklist)
            habit.highest_break = len(streaklist) -1
            habit.last_streak = streaklist[-1]
            streak_ongoing = self.check_ongoing_streak(habit, delta)
            if printit == "all":
                print(habit.name)
                print('Streaklist: ', streaklist)
                print('Highest Streak: ', habit.highest_streak)
            if mode == "max":
                if habit.highest_streak > maxstreak:
                    maxstreak = habit.highest_streak
                    maxstreak_habitname = habit.name
            if printit == str(habit.id) and mode == "streak":
                print(habit.name)
                print("Your streaks of habit " + habit.name + ":" + str(streaklist))
                print('Highest Streak: ', habit.highest_streak)
                if streak_ongoing:
                    print('Current Streak: ', habit.last_streak)
                else:
                    print('Streak broken')
            if mode == "h_break":
                if habit.highest_break > maxbreak:
                    maxbreak = habit.highest_break
                    maxbreak_habitname = habit.name
        if mode == "max":
            if str(maxstreak) == '0':
                print('You have no streaks.')
            else:
                print("Your highest streak is " + str(maxstreak) + " with habit " + maxstreak_habitname + "!")
        if mode == "h_break":
            if str(maxbreak) == '0':
                print('You never broke a habit yet.')
            else:
                print("You have most trouble with habit " + maxbreak_habitname + " with " + str(maxbreak) + " breaks!")


    def check_ongoing_streak(self, habit, delta):
        '''Compares the last date of the streaklist from calculate_streaks of every habit with the next temp_date and calculates if the streak has to be checked today to maintain the streak by comparing temp_date with curent_date'''
        if len(habit.habit_checks) > 0:
            last_date = datetime.datetime.strptime(str(habit.habit_checks[-1].created_at).split()[0], '%Y-%m-%d')
            current_date = datetime.datetime.strptime(str(datetime.datetime.now()).split()[0], '%Y-%m-%d')
            temp_date = last_date + datetime.timedelta(days=delta)
            return temp_date >= current_date
        else:
            return False


    def return_pending(self):        # Return all habits which need to be checked today for maintaining the streak. Used in home screen.
        '''Executes calculate_streaks and prints the streaklist in Home screen'''
        self.calculate_streaks("", "all")

    def return_streak(self):        # Return streak of chosen habit
        '''Executes calculate_streaks and prints the streak of the chosen habit'''
        printit = input('Please type in the number of the habit you want to get the streak:')
        self.calculate_streaks("streak", printit)

    def return_max_streak(self):    # Return habit with highest streak
        '''Executes calculate_streaks and prints the max streak of the chosen habit'''
        self.calculate_streaks("max" )

    def return_max_break(self):    # Return habit with most rouble
        '''Executes calculate_streaks and prints the habit name with the most breaks'''
        self.calculate_streaks("h_break")