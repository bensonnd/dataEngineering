#!/bin/python3
from itertools import groupby
from functools import reduce

import math
import os
import random
import re
import sys

def groupingList(list):
    """Counts the number of occurrences of each number, in order"""
    groupbylist = []
    for key, group in groupby(list, lambda x: x):
        var_count = 0
        for num in group:
            var_count += 1
        groupbylist.append([var_count, key])
    return groupbylist

def geometric_progression(list,r):
    """Checks the geometric progression of each triplet within the list, in order"""
    if (list[1][1] == list[0][1] * r ** 1) and (list[2][1] == list[0][1] * r ** 2): return True
    else: return False

# Complete the countTriplets function below.
def countTriplets(arr, r):
    grouplist = groupingList(arr)
    countlist = []  #doesn't check against previous
    #create triplets from grouped list ex. [[1,1],[2,2],[3,2],[1,4]]
    # gives [[1,1],[2,2],[3,2]] and [[2,2],[3,2],[1,4]]
    for i in range(len(grouplist)-2):
        triplet = [grouplist[i],grouplist[i+1],grouplist[i+2]]
        countlist.append(triplet)
    tripletcount = []
    #check each succession of geometric progression
    newcountlist = []
    for i in countlist:
        templistcount = []
        #drop any triplet that is not a geometric progression
        if geometric_progression(i,r):
            for jind, j in enumerate(i):
                templistcount. append(i[jind][0])
            newcountlist.append(templistcount)
    for i in newcountlist:
        #multiply the grouped, filtered geometric progressions by key count from groupingList
        prod = reduce(lambda x, y: x*y, [j for j in i])
        tripletcount.append(prod)
    return sum(tripletcount)

#arr[0]*r^(5-1)

nr = input().rstrip().split()
n = int(nr[0])
r = int(nr[1])
arr = list(map(int, input().rstrip().split()))
print(arr)
ans = countTriplets(arr, r)
print(ans)
