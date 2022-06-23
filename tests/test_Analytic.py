'''Testing functions of the Analytic module'''
import pytest
from Analytic import *
analytic=Analytic()
from test_Database import *
database=Database()

def pull_habits():
    '''Pull all habit information as instance of a class for the processing layer '''
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits')
    habits = cur.fetchall()
    result = []
    for habit in habits:
        temp_habit = Habit(habit[1], habit[2], habit[3], habit[0], habit[4])
        result.append(temp_habit)
    return result

def pull_checks():
    '''Pull all check information as instance of a class for the processing layer '''
    conn = sqlite3.connect('habit_db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM habit_checks')
    checks = cur.fetchall()
    result = []
    for check in checks:
        temp_check = Check(check[0], check[1], check[2])
        result.append(temp_check)
    return result

def sort_data():
    habits = pull_habits()
    checks = pull_checks()
    for habit in habits:
        for check in checks:
            if check.habit_id == habit.id:
                habit.habit_checks.append(check)
    return habits

def check_ongoing_streak(habit, delta):
    '''Compares the last date of the streaklist from calculate_streaks of every habit with the next temp_date and calculates if the streak has to be checked today to maintain the streak by comparing temp_date with curent_date'''
    if len(habit.habit_checks) > 0:
        last_date = datetime.datetime.strptime(str(habit.habit_checks[-1].created_at).split()[0], '%Y-%m-%d')
        current_date = datetime.datetime.strptime(str(datetime.datetime.now()).split()[0], '%Y-%m-%d')
        temp_date = last_date + datetime.timedelta(days=delta)
        return temp_date >= current_date
    else:
        return False

def calculate_streaks(mode="", printit=""):
    '''For ecery habit check this takes a check as first date, calculates the maximum timepoint for the next check according to the period delta as temp_date and compares it to actual next check second_date'''
    '''If the streak is maintained, the streak counter in streaklist will increase by one. If not, a new 0 will be appended to the list. So the current and highest streak are calculated and the length of the list -1 is the number of breaks.'''
    habits = sort_data()
    maxstreak = -1
    maxstreak_habitname = ""
    maxbreak = -1
    maxbreak_habitname = ""
    checklist_return_pending = []  # Gathers all results to assert return_pending at the end.
    for habit in habits:
        if habit.period == "daily":
            delta = 1
        if habit.period == "weekly":
            delta = 7
        streaklist = [0]
        for i in range(len(habit.habit_checks) - 1):
            first_date = datetime.datetime.strptime(str(habit.habit_checks[i].created_at).split()[0], '%Y-%m-%d')
            second_date = datetime.datetime.strptime(str(habit.habit_checks[i + 1].created_at).split()[0], '%Y-%m-%d')
            temp_date = first_date + datetime.timedelta(days=delta)
            if temp_date >= second_date:
                streaklist[-1] += 1
            else:
                streaklist.append(0)
        habit.highest_streak = max(streaklist)
        habit.highest_break = len(streaklist) - 1
        habit.last_streak = streaklist[-1]
        streak_ongoing = check_ongoing_streak(habit, delta)
        if printit == "all":
            checklist_return_pending.append(habit.name)
            checklist_return_pending.append(streaklist)
            checklist_return_pending.append(habit.highest_streak)
        if mode == "max":
            if habit.highest_streak > maxstreak:
                maxstreak = habit.highest_streak
                maxstreak_habitname = habit.name
        if printit == '1':
            if printit == str(habit.id) and mode == "streak":
                assert habit.id == 1
                assert habit.name == 'Teeth'
                assert str(streaklist) == '[27]'
                assert habit.highest_streak == 27
                assert habit.last_streak == 27
        if printit == '2':
            if printit == str(habit.id) and mode == "streak":
                assert habit.id == 2
                assert habit.name == 'Garbage'
                assert str(streaklist) == '[3]'
                assert habit.highest_streak == 3
                assert habit.last_streak == 3
        if printit == '3':
            if printit == str(habit.id) and mode == "streak":
                assert habit.id == 3
                assert habit.name == 'Bathroom'
                assert str(streaklist) == '[3]'
                assert habit.highest_streak == 3
        if printit == '4':
            if printit == str(habit.id) and mode == "streak":
                assert habit.id == 4
                assert habit.name == 'Pets'
                assert str(streaklist) == '[10, 2, 2, 2, 3]'
                assert habit.highest_streak == 10
                assert habit.last_streak == 3
        if printit == '5':
            if printit == str(habit.id) and mode == "streak":
                assert habit.id == 5
                assert habit.name == 'Training'
                assert str(streaklist) == '[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'
                assert habit.highest_streak == 0
        if mode == "h_break":
            if habit.highest_break > maxbreak:
                maxbreak = habit.highest_break
                maxbreak_habitname = habit.name
    if mode == "max":
        assert str(maxstreak) == '27'
        assert maxstreak_habitname == "Teeth"
    if mode == "h_break":
        assert str(maxbreak) == '13'
        assert maxbreak_habitname == "Training"
    if printit == "all":
        assert str(checklist_return_pending) == "['Teeth', [27], 27, 'Garbage', [3], 3, 'Bathroom', [3], 3, 'Pets', [10, 2, 2, 2, 3], 10, 'Training', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]"

def test_return_pending():  # Return all habits which need to be checked today for maintaining the streak. Used in home screen.
    '''Executes calculate_streaks and prints the streaklist in Home screen'''
    calculate_streaks("", "all")

def test_return_streak():  # Return streak of chosen habit
    '''Executes calculate_streaks and prints the streak of the chosen habit'''
    calculate_streaks("streak", '1')
    calculate_streaks("streak", '2')
    calculate_streaks("streak", '3')
    calculate_streaks("streak", '4')
    calculate_streaks("streak", '5')

def test_return_max_streak():  # Return habit with highest streak
    '''Executes calculate_streaks and prints the max streak of the chosen habit'''
    calculate_streaks("max")

def test_return_max_break():  # Return habit with most rouble
    '''Executes calculate_streaks and prints the habit name with the most breaks'''
    calculate_streaks("h_break")


