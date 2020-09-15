#!/usr/bin/env python3
"""

A "session", unless otherwise noted, represents a focused 25 minute block of time.

    Usage:

        # Print out current goals:
            $ goals

        # Add new goals:
            $ goals add <GOAL>
        
        # Mark goal progress
            $ goals edit <GOAL>

        # See notes on a goal
            $ goals details <GOAL>

        # Set timer to focus on a goal
            $ goals timer <TIME>
"""

import json
import sys
import os
import random

from datetime import datetime

# _______________________________________________________________________
# Constants and Globals

DEBUG_MODE = True

_goals = None

FILENAME = '~/goals.json'
WIDSOM = '~/wisdom.txt'
CHIME = '~/chime.mp3'

# Set to top level directory. For my local machine, these paths resolve to
# /Users/willnowak

PATH = os.path.expanduser(FILENAME)
PATH_OF_WISDOM = os.path.expanduser(WIDSOM)
CHIMEPATH = os.path.expanduser(CHIME)

# _______________________________________________________________________
# Functions

def dbg_print(*args):
    if DEBUG_MODE:
        print(*args)

def get_goals():
    """
    Load goals from ~/goals.json.
    """

    global _goals

    if _goals is not None:
        dbg_print("Goals is not None, they are", _goals)
        return _goals

    if os.path.isfile(PATH):
        with open(PATH, 'r') as f:
            _goals = json.load(f)
    else:
        print("You need a `goals.json` file in your home dir. Something like `$ cd ~ ; echo '{}' >> goals.json` should do the trick.")
        exit()

    return _goals

def write_goal_file(dic, filename=None):

    if os.path.isfile(PATH):
        with open(PATH, 'w') as outfile:
            json.dump(dic, outfile)
    else:
        print("You need a `goals.json` file in your home dir.")
        exit()

def get_today():
    year, week_num, _ = datetime.now().isocalendar()
    return str(year), str(week_num)

def assign_units(goal, units=None):
    if units is None:
        if goal[-1]=='s':  # E.g. goal is meetingS, then 5 meetings are units.
            units = goal
        elif goal == 'ride':
            units = 'miles'
        else:
            units = 'sessions'
    return units

def set_goals():

    global _goals

    dbg_print("Setting goals:")

    full_dict      = get_goals()
    year, week_num = get_today()

    goal     = sys.argv[2]
    quantity = input("What is quantity? ").strip()
    units    = input("What units? ").strip()
    units    = assign_units(goal)
    

    # For each goal set, a sub dictionary with details about it. 
    goal_details              = {}
    goal_details["quantity"]  = quantity
    goal_details["units"]     = units
    goal_details["completed"] = 0

    goal_dict = {goal : goal_details}

    # This is super ugly, but works.
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

def most_popular(full_dict):
    from collections import Counter
    all_goals = []
    for year in full_dict.keys():
        for week in full_dict[year].keys():
            for goal in full_dict[year][week].keys():
                all_goals.append(goal)
    most_common_goals = [i[0] for i in Counter(all_goals).most_common(5)]

    return most_common_goals

def print_wisdom():
    with open(PATH_OF_WISDOM, 'r') as f:
        wisdom_list = f.readlines()
    print('\n****', random.sample(wisdom_list, 1)[0][:-1], '****\n')

def return_goal_list(week=None):
    """
    Function to return goals as a string for autocomplete.

    See README and `goalcomplete.bash` for details.
    """

    if week is None:
        year, week_num = get_today()
    else:
        year, week_num = week[0], str(week[1])

    full_dict = get_goals()
    s = " ".join(list(full_dict[year][week_num].keys()))
    print(s)


def list_goals(all = False, week=None):
    
    print_wisdom()

    if week is None:
        year, week_num = get_today()
    else:
        year, week_num = week[0], str(week[1])

    full_dict = get_goals()
    
    try:
        goals = list(full_dict[year][week_num].keys())
        for i, goal in enumerate(goals):
            print(str(i+1)+
                ". "+
                goal+ 
                ': '+ 
                str(full_dict[year][week_num][goal]['completed'])+
                '/'+
                str(full_dict[year][week_num][goal]['quantity'])+
                ' '+
                str(full_dict[year][week_num][goal]['units']))
        return goals

    except KeyError:
        most_common_goals = most_popular(full_dict)
        print("""   As of yet, no goals for week of {}th week of {}.
    Use `$ goals add` to add some!
    Popular goals include {}. \n""".format(week_num, year, most_common_goals))

def edit_goals(todo, goal=None):
    try:
        goal = str(sys.argv[2])
    except IndexError:
        print("Need to provide a goal to edit. Try `$ goals` to see goals to choose from.")
        return 

    full_dict = get_goals()
    year, week_num = get_today()

    this_week = full_dict.get(year).get(week_num).get(goal)
    try:
        print('So far, completed: ' + str(this_week['completed']))
    except:
        print('So far, completed: 0')

    if todo == 'edit':
        quantity = input("What is quantity completed? ")

        full_dict[year][week_num][goal]['completed'] = quantity
        write_goal_file(full_dict)

        print("You have completed {} out of {} {} for the week.".format(quantity, full_dict[year][week_num][goal]['quantity'], full_dict[year][week_num][goal]['units']))
    elif todo == 'notes':
        notes = input("Add notes:")

        try:
            full_dict[year][week_num][goal]['notes'].append(notes)
        except:
            full_dict[year][week_num][goal]['notes'] = [notes]
        
        write_goal_file(full_dict)

# def set_day_goals():
#     import numpy as np

#     global day_goals

#     try:
#         with open("day.txt", "r") as file:
#             day_goals = eval(file.readline())
#             time_stamp = day_goals[-1]
#             if datetime.now().isocalendar() != time_stamp:
#                 day_goals = []
#     except:
#         day_goals = []

#     try:
#         day_goals.pop()
#     except:
#         print("No list to pop.")

#     inputt = '.'
#     while inputt != '':
#         inputt = input("Day goal? ").strip()
#         day_goals.append(inputt)

#     import time
#     day_goals[-1] = datetime.now().isocalendar()

#     with open("day.txt", "w") as file:
#         file.write(str(day_goals))


# def get_day_goals():
#     with open("day.txt", "r") as file:
#         data2 = eval(file.readline())
#     print(data2[:-1])  # Leave off time stamp.

def list_notes(goal):
    full_dict = get_goals()
    year, week_num = get_today()
    try:
        print(full_dict[year][week_num][goal]['notes'])
    except:
        print("No notes for this goal.")

def start_timer(n=None, s=None):
    '''
    Copied from

    https://stackoverflow.com/questions/15802554/how-to-make-a-timer-program-in-python
    '''
    import sys
    import time
    import os

    counter=0
    s = 0
    m = 0
    len_n = len(str(n))
    initial_n = n
    if not n:
        n = input("Set number of minutes (25 is default): ")
    if n=='':  # Set default.
        n=25
    else:
        n=int(n)
    print("")

    while counter < n*60:
            try:
                # Using this rjust hack. Otherwise I was getting lagging `s` when the string shortened in length.
                print('Time remaining: ' + str(n-m-1).rjust(len_n) + ' minutes, ' + str(60-s).rjust(2) + ' seconds')
                sys.stdout.write("\x1b[1A\x1b[2k")
                time.sleep(1)
                s += 1
                counter+=1
                if s == 60:
                    if m<n+1:
                        m += 1
                    else:
                        m=n
                    s = 0
            except KeyboardInterrupt:
                print("\n\nInterrupted with {} minutes remaining. Go be nice and take care of what needs tending to, and then come back and finish focus block!".format(n-m-1))
                sys.exit(0)

    print("\nTime Is Over Sir! Timer Complete!\n")
    # Play sound.
    from playsound import playsound
    playsound(CHIMEPATH)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        list_goals()
    elif sys.argv[1] in ['help','-h','--help']:
        print(__doc__) 
    elif sys.argv[1] in ['edit', 'e']:
        edit_goals('edit')
    # elif sys.argv[1] == 'day':
    #     set_day_goals()
    # elif sys.argv[1] == 'list_day':
    #     get_day_goals()
    elif sys.argv[1] == 'notes':
        edit_goals('notes')
    elif sys.argv[1] == 'details':
        list_notes(sys.argv[2])
    elif sys.argv[1] == 'add':
        set_goals()
    elif sys.argv[1] == 'timer':
        try:
            n = sys.argv[2]
        except:
            n = None
        start_timer(n)
    elif sys.argv[1] == 'return_goal_list':
        return_goal_list()
    elif sys.argv[1] == 'last_week':
        print("Last week!")
        year, week_num = get_today()
        last_week = (year, str(int(week_num)-1))
        list_goals(week = last_week)

