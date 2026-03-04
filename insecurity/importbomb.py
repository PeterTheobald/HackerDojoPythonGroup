# This module does things as soon as it is imported, you don't have to call any functions

import os

print("**** I AM RUNNING IN YOUR SYSTEM BEFORE YOU EVEN CALL IMPORTED FUNCTIONS ****")
os.system("ls -l")

def first(l):
    return l[0]

def second(l):
    return l[1]

def rest(l):
    return l[1:]


