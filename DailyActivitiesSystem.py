# Anders Lindh
# 2022-01-11

import argparse

def getActivities(file=None):
	if file == None:
		print("no filename provided, use default")
		activities={"Mindfulness": [10,11], "Read": [15, 7], "Pybites": [15, 0], "workout": [10, 0]}
	else:
		print("file provided")
	return activities

activities = getActivities()

parser = argparse.ArgumentParser(description='Support system to execute daily activities')
parser.add_argument("-l", "--list", action='store_true', help='List remaining activities for today')
parser.add_argument('-t', '--today', action='store_true', help='Show all activities for today')
#parser.add_argument('a', help="hej")
parser.add_argument('-a', '--add', help="Add activity for today in order", nargs=2, metavar=("activity","order"))
parser.add_argument('-d', '--done', help="Mark activity as done for today", metavar="activity")
parser.add_argument('-x', '--time', help="Mark activity with time spent", nargs=2, metavar=("activity", "time"))
parser.print_help()  # debug                  
args = parser.parse_args()
if args.list:
	print("List selected")
	for act,time in activities.items():
		if time[1]<time[0]:
			print(act, time[0]-time[1], "minutes left")
if args.today:
	print("show todays activities, regardless their status")
	print(activities)
	for act,time in activities.items():
		print(act, "\t", time[0], "minutes planned", "\t", time[1], "minutes done today")
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

print(activities)

#print("testing")
#print("new line")


