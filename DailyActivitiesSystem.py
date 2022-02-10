#! /usr/bin/env python3
# Anders Lindh
# 2022-01-11

import argparse
import random
import datetime
import os.path
import json
import getpass
import smtplib
import ssl

def getMinutesOrder():
	time_add = input("How many minutes planned? (5) ") or 5
	max_order = printOrder()
	order_add = input("Which order? ("+str(max_order)+") ") or max_order
#	print(time_add, order_add)
	return time_add, order_add

def getActTimeLeft():
	res = ""
	for act in activities_list:
		if act["Time_done"] < act["Time_planned"]: #only activities with time left
			res = res + act["Event"] + " " + str(act["Time_planned"] - act["Time_done"]) + " minutes left\n"
	return res

def getEmailProperties():
	checkEmailFileExists()
	with open("email.json", 'r') as file:
		email = json.loads(file.read())	
	emailAddrS = email["emailAddressSender"]
	smtp = email["SMTP"]
	passw = email["pass"]
	emailAddrR = email["emailAddressReceiver"]
	return emailAddrS, smtp, passw, emailAddrR

def checkEmailFileExists():
	if not (os.path.exists('email.json')):
		createEmailFile()
	return True

def createEmailFile():
	emailAddressSender = input("Enter the sender email address: ")
	smtp = input("Enter the SMTP address: ")
	passw = getpass.getpass(prompt="Type the password for sender accout: ")
	emailAddressReceiver = input("Enter the receiver email address: ")
#add more fields that are needed
	email = {"emailAddressSender": emailAddressSender, "SMTP": smtp, "passw": passw, "emailAddressReceiver": emailAddressReceiver}
	writeToJSON(email, 'email.json')
#maybe check if fields are correct, how?
	return True

def checkLogExists():
	if not (os.path.exists('log.txt')):
		time = convTimeToStr(getTime()) + "\n"
		writeToLog(time)

def getLastTimestamp():
	with open('log.txt', 'r') as file:	#get date of last log entry
		last_time = file.readlines()[-1]
#		print(last_time.rstrip())
	return convTimeToObj(last_time.rstrip())

def checkNewDay():
	checkLogExists()
	last_timestamp = getLastTimestamp()  
	last_date = last_timestamp.date()

	timestamp=getTime()	#get current date and time for log entry
	current_time = convTimeToStr(timestamp)
	date_today = timestamp.date()

	diff = date_today - last_date
	if (diff.days > 0):
		print(diff.days, "days since last log entry")
	return diff.days


def addActivity(activity, order, time):
	for act in activities_list:
		if act["Event"].lower() == activity.lower():
			print("Activity " + activity + " already exists in list")
			return	
	new_act={'ID': 0, 'Event': activity, 'Time_planned': int(time), 'Time_done': 0, 'Order': int(order), 'Periodicity': 1, 'Weekdays': 0, 'Day_counter': 0}
	print("add " + activity)
	activities_list.append(new_act)
	text = activity + " added to todays list\n" + convTimeToStr(getTime()) + "\n"
	writeToLog(text)
	writeToJSON(activities_list, "today.json")
	checkOrder(activities_list)
	return

def writeToLog(text):
	with open('log.txt', 'a') as file:
		file.write(text)
	return 

def writeToJSON(text, file_name):
	with open(file_name, 'w') as file:
		file.write(json.dumps(text,indent=4))
	return
	
def checkBlockExists():
	if not os.path.exists("block.json"):	
		activities_list=[{"ID": 0, "Event": "Mindfulness", "Time_planned": 10, "Time_done": 10, "Order": 1, "Periodicity": 1, "Weekdays": 0, "Day_counter": 0}, {"ID": 1, "Event": "Read", "Time_planned":15, "Time_done": 0, "Order": 0, "Periodicity": 2, "Weekdays": 0, "Day_counter": 0},{"ID": 2, "Event": "Eat fruit", "Time_planned": 5, "Time_done": 0, "Order": 0, "Periodicity": 1, "Weekdays": 0, "Day_counter": 0}, {"ID": 3, "Event": "Python", "Time_planned": 20, "Time_done": 0, "Order": 2, "Periodicity": 2, "Weekdays": 0, "Day_counter": 0}]
		writeToJSON(activities_list, "block.json")

def checkTodayExists():
	if not os.path.exists("today.json"):	
		with open("block.json", 'r') as file:
			activities_list = json.loads(file.read())	
		result_weekdays = checkWeekdays(activities_list)
		while result_weekdays != True:
			print("Error in weekdays")
			print(result_weekdays["Weekdays"])
			#exit(1)	#weekdays wrong, fix
			fixWeekdays(result_weekdays, True) 	
			result_weekdays = checkWeekdays(activities_list)
		writeToJSON(activities_list, "block.json")
		writeToJSON(activities_list, "today.json")

def getActivities(days,file_name):
	checkBlockExists()
	checkTodayExists()
	with open(file_name, 'r') as file:
		activities_list = json.loads(file.read())
			#print(activities_list)
	for act in activities_list:
		act["Time_planned"] = int(act["Time_planned"])
		act["Time_done"] = int(act["Time_done"])
		act["Order"] = int(act["Order"])
		act["Periodicity"] = int(act["Periodicity"])
		act["Day_counter"] = int(act["Day_counter"])+days
	
	act_list2=[]
	if days > 0:
		text = "New day\n" + convTimeToStr(getTime()) + "\n"
		writeToLog(text)
		for act in activities_list:
			if act["Weekdays"] == 0:
				if act["Day_counter"] >= act["Periodicity"]:
					act["Time_done"] = 0
					act["Day_counter"] = 0
					act_list2.append(act)
			else:
				weekday = getTime().isoweekday()
				#print("weekday", weekday, "act[\"Event\"]", act["Event"], "act[\"Weekdays\"]", act["Weekdays"])	#debug
				if weekday in act["Weekdays"]:
					act["Time_done"] = 0
					act_list2.append(act)
		writeToJSON(activities_list, 'block.json')
		return act_list2
	return activities_list

def sort(activities_list):
	if checkOrder(activities_list) == True: #check if every "Order" is unique except for 0, which is a flag for random order
		activities_list.sort(key=lambda item: item.get("Order")) 
		ID = 1
		for item in activities_list:
			if item["Order"] > 0:	#set ID if order is fixed (not random)
				item["ID"] = ID
				ID += 1
		start = ID	#get start value for random activities (next value after the fixed ones)
		stop = len(activities_list)+1 #get stop value
		#print("start", start, "stop", stop)
		#print(random.randrange(start, stop))
		#print(list(range(start,stop)))	
		#print(random.choice(range(start, stop)))
		random_activities=list(range(start, stop))	#create list of possible random ID:s 
		#print(random_activities, random.choice(random_activities))
		for item in activities_list:	#go through activities again, but check for those marked with random this time
			if item["Order"] == 0:
				random_ID = random.choice(random_activities) #pick one of the remaining places for the activity
				item["ID"] = random_ID
				random_activities.remove(random_ID)	#remove the used value
		activities_list.sort(key=lambda item: item.get("ID"))	#sort again, this time by ID now that the random ID:s are in place

		return activities_list

def checkOrder(activities_list):
	res_list = []	#temporary list, will hold values of "Order" which are fixed (not random which have "Order" == 0)
	for act in activities_list:
		current = act["Order"]
		if current > 0:
			if current in res_list:	#the value of "Order" exists for another entry
				fix_order = input("Order not unique, fix (Y/n)? ") or "Y"
				if fix_order.upper() == "Y":
					fixOrder()
					checkOrder(activities_list)
				else:
					return False, act["Event"]	#exit the check, send the value of the second "Event" with the same "Order"
			res_list.append(current)
	writeToJSON(activities_list, 'today.json')
	return True
	
def fixOrder():
	for act in activities_list:
		print(act["Event"], "Order", act["Order"])
	for act in activities_list:
		order=input(act["Event"] + " desired order (" + str(act["Order"]) + ") ") or act["Order"]
		act["Order"] = int(order)
	#if not checkOrder(activities_list):
		#exit(1) #still not ordered, exit program

def fixWeekdays(act, error_mode):
	if error_mode:
		if type(act["Weekdays"]) == int:
			scheduled = " not "
		elif type(act["Weekdays"]) == list:
			scheduled = " "
		else:
			scheduled = " possibly "
		print(act["Event"] + " currently" + scheduled + "set to run on specific weekdays, but with some error")
	result = input("Do you want it to be scheduled for fixed weekdays (Y/n)? ") or "Y"
	if result.upper() == "Y":
		day_counter = 1
		res_weekday = []
		for day in ["monday", "tuesday", "wednesday", "thursdag", "friday", "saturday", "sunday"]:
			res = input("Do you want " + act["Event"] + " scheduled for " + day + " (Y/n)? ") or "Y"
			if res.upper() == "Y":
				res_weekday.append(day_counter)
			day_counter += 1
		act["Weekdays"] = res_weekday
	else:
		act["Weekdays"] = 0
		if not error_mode:
			fixPeriodicity(act)
		checkPeriodicity(act)
	#print("Corrected value: " + str(act["Weekdays"]))
	return True
	
def checkPeriodicity(act):
	if type(act["Periodicity"]) == int:
		if act["Periodicity"] < 1:
			fixPeriodicity(act)
			checkPeriodicity(act)
	else: 
		fixPeriodicity(act)
		checkPeriodicity(act)
	return True

def fixPeriodicity(act):
	if act["Periodicity"] > 0:
		per = act["Periodicity"]
	else:
		per = 1
	res_per = input("How often do you want to run " + act["Event"] + " (" + str(per) + ") day? ") or per
	act["Periodicity"] = int(res_per)
	return True

def checkWeekdays(activities_list):	
	for act in activities_list:
		#print(act["Event"])
		if type(act["Weekdays"]) == int:
			#print("Weekdays = int")
			if act["Weekdays"] != 0:
				return act
		elif type(act["Weekdays"]) == list:
			#print(act["Weekdays"])
			if max(act["Weekdays"]) > 7 or min(act["Weekdays"]) < 1:
				return act
		else:
			return act
	return True				

def getTime():
	return datetime.datetime.now()	#get current date and time for log entry

def convTimeToStr(time):
	return time.strftime("%Y-%m-%d %H:%M:%S")

def convTimeToObj(time):
	return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def printOrder():
	order = 0
	for act in activities_list:
		print(act["Event"], "order", act["Order"])
		if act["Order"] > 0:
			order += 1
	return order+1

days = checkNewDay()
if days != 0:
	if os.path.exists('today.json'):
		os.remove('today.json')
activities_list = getActivities(days,"today.json")	#at start of script, if new day reset Time_done and increase Day_counter
sort(activities_list)	#at start of day or if requested with -
parser = argparse.ArgumentParser(description='Support system to execute daily activities')
parser.add_argument("-l", "--list", action='store_true', help='List remaining activities for today')
parser.add_argument('-t', '--today', action='store_true', help='Show all activities for today')
parser.add_argument('-a', '--add', help="Add activity for today in order", nargs=3, metavar=("activity","order","time_planned"))
parser.add_argument('-d', '--done', help="Mark activity as done for today", metavar="activity")
parser.add_argument('-x', '--time', help="Mark activity with time spent", nargs=2, metavar=("activity", "time"))
parser.add_argument('-c', '--change', action='store_true', help="Change order for todays activities")
parser.add_argument('-s', '--shuffle', action='store_true', help='Shuffle the unordered activities for today')
parser.add_argument('-e', '--email', action='store_true', help='Load and Check email properties')
parser.add_argument('-b', '--block', action='store_true', help='Edit block file (the recurring activities)')

#parser.print_help()  # debug                  
args = parser.parse_args()
if args.block:
	checkBlockExists()
	activities_list = getActivities(0,"block.json")
	menu = 1
	while menu != 0:
		#clear screen?
		print("Edit the blocks of recurring activities")
		print("1 Add new activity")
		print("2 Remove activity")
		print("3 Change order")
		print("4 Change periodicity/weekdays")
		print("5 Change time planned")
		print("0 quit")
		menu = int(input("Select 1-5 "))
		if menu == 1:
			print("Add new activity")
			new_act = input("Enter name for new activity: ")
			time_add, order_add = getMinutesOrder()
			addActivity(new_act, order_add, time_add) 
			writeToJSON(activities_list, "block.json")
		if menu == 2:
			remove = False
			print("Remove activity")
			for act in activities_list:
				res = input("Remove " + act["Event"] + "? (y/N) ") or "N"
				if res.lower() == "y":
					activities_list.remove(act)
					print(activities_list)
					remove = True
			if remove == True:
				writeToJSON(activities_list, "block.json")

		if menu == 3:
			print("Change order")
			fixOrder()
			writeToJSON(activities_list, "block.json")
		if menu == 4:
			print("change periodicity or weekday")
			for act in activities_list:
				text = "Change " + act["Event"] + " with current settings: "
				if act["Weekdays"] == 0:
					text = text + "periodicity " + str(act["Periodicity"])
				else:
					text = text + "weekdays " + str(act["Weekdays"])
				res = input(text + " (y/N) ") or "N"
				if res.upper() == "Y":
					fixWeekdays(act, False)		
			writeToJSON(activities_list, "block.json")
		if menu == 5:
			print("Add new activity")
	print("quit")
	exit(0)
if args.email:
	print("Load email properties")
	emailS, smtp, passw, emailR = getEmailProperties()
	actLeft = getActTimeLeft()
	if len(actLeft) > 0:
		message = "Subject: Activities with time left today\n\n" + convTimeToStr(getTime()) + "\n" + getActTimeLeft()
	else:
		
		message = "Subject: All Activities done!\n\n" + convTimeToStr(getTime()) + "\n" + "Well done! Keep up the good work!"
	# read more about sending emails at https://realpython.com/python-send-email/
	port = 465
	context = ssl.create_default_context()
	print("Send email to " + emailR)
	with smtplib.SMTP_SSL(smtp, port, context=context) as server:
		server.login(emailS, passw)
		server.sendmail(emailS, emailR, message)
if args.shuffle:
	print("Rerun shuffle for the unordered activities")
	sort(activities_list)
if args.list:
	print("Show remaining activities for today")
	print(getActTimeLeft())
#	for act in activities_list:
#		if act["Time_done"] < act["Time_planned"]: #only activities with time left
#			print(act["Event"], act["Time_planned"] - act["Time_done"], "minutes left")
if args.today:
	print("Show todays activities, regardless their status")
	for act in activities_list:
		print(act["Event"] + ": [" + str(act["Time_planned"]) + " minutes planned] " + str(act["Time_done"]) + " minutes done today")

if args.change:
	print("Change order for todays activities")
	fixOrder()
	checkOrder(activities_list)
#if args.check: # remove arg, run at startup instead. Check both blockfile and today and activities_list. Check order and weekdays
	#print("Check if blockfile is OK regarding order")
	#print(checkOrder(activities_list))
if args.add:
	addActivity(args.add[0],args.add[1],args.add[2])

if args.done: 
	for act	in activities_list:
		if act["Event"].lower() == args.done.lower():
			print("done", args.done)
			act["Time_done"] = act["Time_planned"]
			text_to_logfile = act["Event"] + " done at \n" + convTimeToStr(getTime()) + "\n"
			writeToLog(text_to_logfile)
			writeToJSON(activities_list, "today.json")

if args.time:	
	found = False
	for act in activities_list:
		if act["Event"].lower() == args.time[0].lower():
			found = True
			print(args.time[1], "minutes spent on", args.time[0])
			act["Time_done"] = int(args.time[1]) + int(act["Time_done"])
			text_to_logfile = args.time[1] + " minutes spent on " + act["Event"] + " at \n" + convTimeToStr(getTime()) + "\n"
			writeToLog(text_to_logfile)
			writeToJSON(activities_list, "today.json")
	if found == False:
		add_answer = input("Activitity " + args.time[0] + " was not found. Add it for today (Y/n)?") or "Y"
		if add_answer.upper() == "Y":
			time_add, order_add = getMinutesOrder()
#			time_add = input("How many minutes planned? (5) ") or 5
#			max_order = printOrder()
#			order_add = input("Which order? ("+str(max_order)+") ") or max_order
#			print(time_add, order_add)
			addActivity(args.time[0], order_add, time_add)
			
		#input

#checkNewDay()

#with open('log.txt', 'r') as file:	#get date of last log entry
#	last_time = file.readlines()[-1]
#	print(last_time.rstrip())
#last_timestamp = convTimeToObj(last_time.rstrip())

##print(activities_list)
#timestamp=getTime()	#get current date and time for log entry
#current_time = convTimeToStr(timestamp)
#print(current_time)
#with open('log.txt', 'a') as file:   #only when checking days passed
#	file.write("No argument passed\n")
#	file.write(current_time+"\n")


#diff = timestamp - last_timestamp
#if (diff.days == 0):
#	print("Still the same day!")
#else:
#	print(diff.days, "days since last log entry")
##print("testing")
##print("new line")


