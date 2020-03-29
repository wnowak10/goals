#!/usr/bin/env python3
"""
    Usage:

        # Print out current goals:
            $ goals

        # Add new goals:
            $ goals add
        
        # Mark goal progress
            $ goals edit <GOAL>
        
        # Learn more about a specific goal
            $ goals details <GOAL>
"""

import json
import pandas as pd
from datetime import datetime
import sys
import os

# _______________________________________________________________________
# Constants and Globals

DEBUG_MODE = True

_goals = None

FILENAME = '~/goals.json'
PATH = os.path.expanduser(FILENAME)

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

    if os.path.isfile(PATH):
        with open(PATH, 'r') as f:
            _goals = json.load(f)
    else:
        print("You need a `goals.json` file in your home dir.")
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
    # return year, week_num

# Run on Sunday
def set_goals():

    global _goals

    dbg_print("Setting goals:")

    full_dict = get_goals()

    year, week_num = get_today()

    goal     = input("What is your weekly goal? ").strip()
    quantity = input("What is quantity? ")
    units    = input("What units? ")

    # For each goal set, a sub dictionary with details about it. 
    goal_details = {}
    goal_details["quantity"] = quantity
    goal_details["units"] = units
    goal_details["completed"] = 0

    goal_dict = {goal:goal_details}

    # this is super ugly, but works.
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
    print("Listing week's goals: ")
    if week is None:
        year, week_num = get_today()

    full_dict = get_goals()

    try:
        goals = list(full_dict[year][week_num].keys())
        for i, goal in enumerate(goals):
            print(i+1, ": ", goal)
        return goals

    except KeyError:
        print("As of yet, no goals for week of {}th week of {}. Use `$ goals add` to add some!".format(week_num, year))

def list_details(goal=None, week_num=None, year=None):
    full_dict = get_goals()
    # dbg_print(full_dict['2020']['13']['ride'])
    if week_num is None and year is None:
        year, week_num = get_today()

    if len(sys.argv) >= 2:
        dbg_print('Getting goal from command line.')
        try:
            goal = full_dict.get(year).get(week_num).get(str(sys.argv[2]))
        except AttributeError:
            print("No goals for this time period.")
    else: 
        goal = full_dict.get(year).get(week_num).get(goal)
    print(goal)

def edit_goals(goal=None):
    try:
        goal = str(sys.argv[2])
    except IndexError:
        print("Need to provide a goal to edit. Try `$goals` to see goals to choose from.")
        return 
    full_dict = get_goals()
    year, week_num = get_today()

    print(full_dict[year][week_num][goal]['completed'])
    
    try:
        this_week = full_dict.get(year).get(week_num)
        quantity = input("What is quantity completed? ")

        full_dict[year][week_num][goal]['completed'] = quantity
        write_goal_file(full_dict)

        print("You have completed {} out of {} {} for the week.".format(quantity, this_week[goal]['quantity'], this_week[goal]['units']))
    except:
        print("You have no goals for this week to edit.")

    
    return
    
if __name__ == '__main__':

    if len(sys.argv) == 1:
        list_goals()
    elif sys.argv[1] in ['help','-h','--help']:
        print(__doc__) 
    elif sys.argv[1] == 'edit':
        edit_goals()
    elif sys.argv[1] == 'add':
        set_goals()
    elif sys.argv[1] == 'details':
        list_details()

