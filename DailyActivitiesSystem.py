# Anders Lindh
# 2022-01-11

import argparse

paser = argparse.ArgumentParser(description='Support system to execute daily activities')
parser.add_argument('list', help='List remaining activities for today')
parser.add_argument('all', help='Show all activities for today')
parser.print_help()                    
