
# -*- coding: utf-8 -*-

# ARGV[0]: number of conferences. default:10

#import sys
#args = sys.argv
#if(len(args) <= 1):
#	print("len(args)[" + str(len(args)) + "] < **")
#	sys.exit()
#if args[1]:
num = 10

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log as l
log = l.getLogger()
log.info("get_papers_from_IEEE.py start.")
log.info("number["+str(num)+"]")

from IEEEXplore import IEEEXplore as X
xplore = X()

xplore.get_papers_of_new_conferences(num)

