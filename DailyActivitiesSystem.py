# Anders Lindh
# 2022-01-11

import argparse
import random

def getActivities(file=None):
	if file == None:
		print("no filename provided, use default")
		activities_list=[{"ID": 0, "Event": "Mindfulness", "Time_planned": 10, "Time_done": 10, "Order": 1, "Periodicity": 1, "Weekdays": 0, "Day_counter": 0}, {"ID": 1, "Event": "Read", "Time_planned":15, "Time_done": 0, "Order": 0, "Periodicity": 2, "Weekdays": 0, "Day_counter": 0},{"ID": 2, "Event": "Eat fruit", "Time_planned": 5, "Time_done": 0, "Order": 0, "Periodicity": 1, "Weekdays": 0, "Day_counter": 0}, {"ID": 3, "Event": "Python", "Time_planned": 20, "Time_done": 0, "Order": 2, "Periodicity": 2, "Weekdays": 0, "Day_counter": 0}]
#		activities={"Mindfulness": [10,11], "Read": [15, 7], "Pybites": [15, 0], "workout": [10, 0]}
	else:
		print("file provided")
	return activities_list

def sort(activities_list):
	print("sort begin")	#debug
	if check_block(activities_list) == True: #check if every "Order" is unique except for 0, which is a flag for random order
		print("Sorting")
		activities_list.sort(key=lambda item: item.get("Order")) 
		ID = 1
		for item in activities_list:
			if item["Order"] > 0:	#set ID if order is fixed (not random)
				item["ID"] = ID
				ID += 1
		start = ID	#get start value for random activities (next value after the fixed ones)
		stop = len(activities_list)+1 #get stop value
		print("start", start, "stop", stop)
		#print(random.randrange(start, stop))
		print(list(range(start,stop)))	
		print(random.choice(range(start, stop)))
		random_activities=list(range(start, stop))	#create list of possible random ID:s 
		print(random_activities, random.choice(random_activities))
		for item in activities_list:	#go through activities again, but check for those marked with random this time
			if item["Order"] == 0:
				random_ID = random.choice(random_activities) #pick one of the remaining places for the activity
				item["ID"] = random_ID
				random_activities.remove(random_ID)	#remove the used value
		activities_list.sort(key=lambda item: item.get("ID"))	#sort again, this time by ID now that the random ID:s are in place

		return activities_list

def check_block(activities_list):
	res_list = []	#temporary list, will hold values of "Order" which are fixed (not random which have "Order" == 0)
	for act in activities_list:
		current = act["Order"]
		if current > 0:
			if current in res_list:	#the value of "Order" exists for another entry
				return False, act["Event"]	#exit the check, send the value of the second "Event" with the same "Order"
			res_list.append(current)
	return True
	

activities_list = getActivities()	#at start of script, if new day reset Time_done and increase Day_counter
sort(activities_list)	#at start of day or if requested with -
print(activities_list)
parser = argparse.ArgumentParser(description='Support system to execute daily activities')
parser.add_argument("-l", "--list", action='store_true', help='List remaining activities for today')
parser.add_argument('-t', '--today', action='store_true', help='Show all activities for today')
#parser.add_argument('a', help="hej")
parser.add_argument('-a', '--add', help="Add activity for today in order", nargs=2, metavar=("activity","order"))
parser.add_argument('-d', '--done', help="Mark activity as done for today", metavar="activity")
parser.add_argument('-x', '--time', help="Mark activity with time spent", nargs=2, metavar=("activity", "time"))
parser.add_argument('-c', '--check', action='store_true', help="Check activities list regarding unique order")
parser.print_help()  # debug                  
args = parser.parse_args()
if args.list:
	print("Show remaining activities for today")
#	for act,time in activities.items():
	for act in activities_list:
	# if time[1]<time[0]:
	#print(act)
	#	print(act.items())
		if act["Time_done"] < act["Time_planned"]: #only activities with time left
			print(act["Event"], act["Time_done"])
#		for key, value in act.items():
#				print(key + ": " + str(value))
#		print(act)
#			print(act, time[0]-time[1], "minutes left")
if args.today:
	print("Show todays activities, regardless their status")
	# print(activities_list)
	for act in activities_list:
		print(act["Event"], "\t", act["Time_planned"], "minutes planned", "\t", act["Time_done"], "minutes done today")
if args.check:
	print("Check if blockfile is OK regarding order")
	print(check_block(activities_list))
if args.add:
	print("add ")
	print(args.add[0])
	print(args.add[1])
if args.done:
	print("done", args.done)
	if args.done in activities: # Need to find a way to check case insensitive
		print("Activity exists")
		print(activities[args.done])
		time_planned=activities[args.done][0]
		print(time_planned)
		activities[args.done][1]=time_planned
		print(activities) # debug, chech change is register

	else:
		print("Activity does not exist in todays planning")
if args.time:
	print(args.time[1], "minutes spent on", args.time[0])
	if args.time[0] in activities:
		print(activities[args.time[0]])
		activities[args.time[0]][1]=activities[args.time[0]][1] + int(args.time[1])

#print(activities_list)

#print("testing")
#print("new line")


