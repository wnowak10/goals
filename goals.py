import json
import pandas as pd
from datetime import datetime


# _______________________________________________________________________
# Constants and Globals

DEBUG_MODE = True

_goals = None

FILENAME = 'goals.json'

# _______________________________________________________________________
# Functions


def dbg_print(*args):
    if DEBUG_MODE:
        print(*args)

def get_goals():

    global _goals

    if _goals is not None:
        dbg_print("Goals is not None, they are", _goals)
        return _goals

    with open(FILENAME, 'r') as f:
        _goals = json.load(f)

    return _goals

def write_goal_file(dic, filename=None):

    with open(FILENAME, 'w') as outfile:
        json.dump(dic, outfile)


# Run on Sunday
def set_goals():

    global _goals

    dbg_print("Setting goals:")

    full_dict = get_goals()

    year, week_num, _ = datetime.now().isocalendar()
    year = str(year)
    week_num = str(week_num)
    # week_num = '1'

    goal     = input("What is your weekly goal? ")
    quantity = input("What is quantity? ")
    units    = input("What units? ")

    # For each goal set, a sub dictionary with details about it. 
    goal_details = {}
    goal_details["quantity"] = quantity
    goal_details["units"] = units

    goal_dict = {goal:goal_details}
    def rec_dd():
        import collections
        return collections.defaultdict(rec_dd)

    try:
        full_dict[year]
    except:
        full_dict[year] = {}
    try:
        full_dict[year][week_num]
        full_dict[year][week_num].update(goal_dict)
    except:
        full_dict[year][week_num] = goal_dict

    _goals = full_dict

    write_goal_file(full_dict)

    return full_dict

def list_goals(all = False, week=None):
    if week is None:
        year, week_num, _ = datetime.now().isocalendar()
        year = str(year)
        week_num = str(week_num)
        # year, week_num, _ = my_date.isocalendar()
        # week = str((year, week_num))

    full_dict = get_goals()

    print("week of :", week_num, '\n')
    goals = full_dict[year][week_num].keys()
    print(goals)
    # try:
    #     goals = full_dict[year][week].keys()
    # except KeyError:
    #     print("no goals for week of {}th week of {}.".format(week_num, year))
    # return

set_goals()
list_goals()

    # print(full_dict[week].keys())

# def edit_goals(goal):
#   my_date = datetime.now()
#   year, week_num, _ = my_date.isocalendar()
#   week_year_tuple = str((year, week_num))

#   with open('goals.json', 'r') as f:
#       full_dict = json.load(f)

#   this_week = full_dict[week_year_tuple]
#   # returns {"goals": [{"units": "miles", "goal": "ride", "quantity": "100"}]
#   this_week['goals']
#   {"week":{"goal":{goal_details}}}


# list_goals(week = (2020, 12))


