# DailyActivitiesOrganizer
Hopefully a system to help me get daily activities done
Python command line interface
Ideas:
one block is an activity i.e. reading, training, learning, clean the desk 5 min and so on
randomly showing the blocks?
cli note a block ready for the day or how many minutes done so far
ordinary order for the blocks
weekly plan for activities that not are on daily basis (every other day (or third and so on), mondays and thursdays)
every block has an estimated time 
logging of status for the blocks at the end of the day (to a file)
mail sent during the day for blocks which are not done yet (scheduled time or random time), perhaps more than one mail per day?
perhaps notifications for ubuntu (not neccesary) 
change order of blocks as priorities change
discharg this days block if it is not relevant or the time flies (a note in the logg that it was on purpose, not just didn't get the time. Could be valuable information)
mail function is a deamon running in the background?
perhaps a weekly mail of status.
logging includes time marked as done
file format? JSON? XML?
files: log file, block file (wiht name of the block, estimated time consumption, order (or ok to put randomly after those with order)

example of how i think the cli will work.
scriptname.py mindfulness done  [mark mindfulness as done for the day] [mindfulness is a blockname]

scriptname.py mindfulness 15  [mark mindfulness as 15 minutes done] if time is greater than estimated time note in logg and mark as done

scriptname.py list [show blocks left today]

scriptname.py today [show all blocks, those done will be marked as done, those with time left will show both time done and time left]

scriptname.py order {blockname} 1 [set blockname as first today, change those beneath. will only affect todays order]
scriptname.py order {blockname} random [set blockname as random after those with fixed positions today, will only affect todays order]

scriptname.py settings [print block file information and how to change the file] Or perhaps change the file


the block file contains a header with information on how to change the file manually (which is the only way?)

