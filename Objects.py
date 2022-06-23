#!/usr/bin/python
"""Make the code able to run in a unix environment"""

"""Objects contains all business objects like habits and classes"""

class Habit:                    # Habit class provides methods for the edit screen.
    """The concept of a habit is encoded in the habit class using object-oriented programming."""
    def __init__(self, name, spec, period, id=None, created_at=None):
        self.name = name
        self.spec = spec
        self.period = period
        self.id = id
        self.created_at = created_at
        self.habit_checks = []
    def __str__(self):
        return f"{self.id} {self.name} {self.spec} {self.period} {self.created_at} {self.habit_checks}"
    def __repr__(self):
        return f"{self.id} {self.name} {self.spec} {self.period} {self.created_at} {self.habit_checks}"

class Check:
    """The concept of a check is encoded in the check class using object-oriented programming."""
    def __init__(self, id, habit_id, created_at):
        self.id = id
        self.habit_id = habit_id
        self.created_at = created_at

    def __str__(self):
        return f"{self.id} {self.habit_id} {self.created_at}"

    def __repr__(self):
        return f"{self.id} {self.habit_id} {self.created_at}"