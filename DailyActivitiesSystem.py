# Anders Lindh
# 2022-01-11

import argparse

parser = argparse.ArgumentParser(description='Support system to execute daily activities')
parser.add_argument("-l", "--list", action='store_true', help='List remaining activities for today')
parser.add_argument('-t', '--today', action='store_true', help='Show all activities for today')
#parser.add_argument('a', help="hej")
parser.add_argument('-a', '--add', help="Add activity in order", nargs=2, metavar=("activity","order"))
parser.print_help()                    
args = parser.parse_args()
if args.list:
	print("List selected")
if args.today:
	print("show todays activities, regardless their status")
if args.add:
	print("add ")
	print(args.add[0])
	print(args.add[1])
#print("testing")
#print("new line")
