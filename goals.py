import json
import pandas as pd
from datetime import datetime


# _______________________________________________________________________
# Constants and Globals

_goals = None

FILENAME = 'goals.json'



def get_goals():

	global _goals

	if _goals is not None:
		return _goals

	with open(FILENAME, 'r') as f:
		_goals = json.load(f)

	return _goals

def write_goal_file(dic, filename=None):

	with open(FILENAME, 'w') as outfile:
	    json.dump(dic, outfile)


# Run on Sunday
def set_goals():
	
	full_dict = get_goals()

	year, week_num, _ = datetime.now().isocalendar()
	week_year_tuple = str((year, week_num))
	print(week_year_tuple)

	goal = input("What is your weekly goal? ")
	quantity = input("What is quantity? ")
	units = input("What units? ")

	# For each goal set, a sub dictionary with details about it. 
	goal_details = {}
	goal_details["quantity"] = quantity
	goal_details["units"] = units

	goal_dict = {goal:goal_details}

	try:
		full_dict[week_year_tuple].update(goal_dict)
	except KeyError:
		full_dict[week_year_tuple] = {}
		full_dict[week_year_tuple].update(goal_dict)

	write_goal_file(full_dict)

	# with open('goals.json', 'w') as outfile:
	#     json.dump(full_dict, outfile)

	return full_dict

def list_goals(week=None):
	if week is None:
		print("NO WEEK")
		my_date = datetime.now()
		year, week_num, _ = my_date.isocalendar()
		week = str((year, week_num))

	full_dict = get_goals()

	print("week of :", week, '\n')
	try:
		goals = full_dict[week].keys()
	except KeyError:
		print("no goals for week of {}".format(week))
	return

set_goals()

	# print(full_dict[week].keys())

# def edit_goals(goal):
# 	my_date = datetime.now()
# 	year, week_num, _ = my_date.isocalendar()
# 	week_year_tuple = str((year, week_num))

# 	with open('goals.json', 'r') as f:
# 	    full_dict = json.load(f)

# 	this_week = full_dict[week_year_tuple]
# 	# returns {"goals": [{"units": "miles", "goal": "ride", "quantity": "100"}]
# 	this_week['goals']
# 	{"week":{"goal":{goal_details}}}


# list_goals(week = (2020, 12))


