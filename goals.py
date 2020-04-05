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
import sys
import os

from datetime import datetime

# _______________________________________________________________________
# Constants and Globals

DEBUG_MODE = False

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

def set_goals():

    global _goals

    dbg_print("Setting goals:")

    full_dict      = get_goals()
    year, week_num = get_today()

    goal     = input("What is your weekly goal? ").strip()
    quantity = input("What is quantity? ").strip()
    units    = input("What units? ").strip()

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

def list_goals(all = False, week=None):
    dbg_print("Listing week's goals: ")
    if week is None:
        year, week_num = get_today()

    full_dict = get_goals()

    try:
        goals = list(full_dict[year][week_num].keys())
        for i, goal in enumerate(goals):
            print(str(i+1)+
                ". "+
                goal+ 
                ': '+ 
                full_dict[year][week_num][goal]['completed']+
                '/'+
                full_dict[year][week_num][goal]['quantity']+
                ' '+
                full_dict[year][week_num][goal]['units'])
        return goals

    except KeyError:
        print("As of yet, no goals for week of {}th week of {}. Use `$ goals add` to add some!".format(week_num, year))

def list_details(goal=None, week_num=None, year=None):
    full_dict = get_goals()

    if week_num is None and year is None:
        year, week_num = get_today()

    if len(sys.argv) >= 2:
        try:
            goal = full_dict.get(year).get(week_num).get(str(sys.argv[2]))
        except AttributeError:
            print("No goals for this time period.")
    else: 
        goal = full_dict.get(year).get(week_num).get(goal)
    print('Completed {} out of {} {}.'.format(goal['completed'], goal['quantity'], goal['units']))

def edit_goals(todo, goal=None):
    try:
        goal = str(sys.argv[2])
    except IndexError:
        print("Need to provide a goal to edit. Try `$goals` to see goals to choose from.")
        return 

    full_dict = get_goals()
    year, week_num = get_today()

    this_week = full_dict.get(year).get(week_num).get(goal)
    print('So far, completed: ' + this_week['completed'])

    if todo=='edit':
        try:
            quantity = input("What is quantity completed?")

            full_dict[year][week_num][goal]['completed'] = quantity
            write_goal_file(full_dict)

            print("You have completed {} out of {} {} for the week.".format(quantity, this_week[goal]['quantity'], this_week[goal]['units']))
        except:
            print("You have no goals for this week to edit.")
    elif todo=='notes':
        notes = input("Add notes:")

        try:
            full_dict[year][week_num][goal]['notes'].append(notes)
        except:
            full_dict[year][week_num][goal]['notes'] = [notes]
        
        write_goal_file(full_dict)

    
    return
    
if __name__ == '__main__':

    if len(sys.argv) == 1:
        list_goals()
    elif sys.argv[1] in ['help','-h','--help']:
        print(__doc__) 
    elif sys.argv[1] == 'edit':
        edit_goals('edit')
    elif sys.argv[1] == 'notes':
        edit_goals('notes')
    elif sys.argv[1] == 'add':
        set_goals()
    elif sys.argv[1] == 'details':
        list_details()

