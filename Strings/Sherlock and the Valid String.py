#!/bin/python3

import math
import os
import random
import re
import sys

from itertools import groupby

# Complete the makeAnagram function below.
def groupingList(list):
    """Group and count each letter's occurrence.
    Paramaters:
    string input, sorted ex: 'aabbccdddd'
    Returns:
    list of counts of each letter ex: [2,2,2,4]"""
    groupbylist = []
    for key, group in groupby(list, lambda x: x[0]):
        var_count = 0
        for num in group:
            var_count += 1
        groupbylist.append(var_count)
    return groupbylist


def checkEqual(iterator):
    """Checks to see if all the values in a list are identical.
    Paramaters:
    list input, ex: [2,2,2,2,2] or [2,2,2,4]
    Returns:
    bool True if all elements are the same"""
    return len(set(iterator)) <= 1

# Complete the isValid function below.
def isValid(s):
    """Checks to see if all letters are unique,
    if all characters of the string appear the same number of times,
    and if remove just one character at any index in the string,
    the remaining characters will occur the same number of times.
    Paramaters:
    string input ex: 'aabbccdddd'
    Returns:
    YES if valid, else NO"""

    # check for to see if length = length of string of unique characters
    if len(s) == len(set(s)): return 'YES'
    grouplist = groupingList(sorted(s))
    m = max(grouplist)
    # check for max values in list
    maxgrouplist = [i for i in grouplist if i == m]
    # remove the max values from the list
    removemaxlist = [i for i in grouplist if i not in maxgrouplist]
    # check to see if there is only one max value, if the remaining values are all the same, and if if the difference between max and remaining unique value is only 1
    if len(maxgrouplist) == 1 and checkEqual(removemaxlist) and (m - next(iter(set(removemaxlist)))) == 1: return 'YES'
    if len(removemaxlist) == 1 and checkEqual(maxgrouplist): return 'YES'
    if grouplist == maxgrouplist: return 'YES'
    else: return 'NO'

s = input()
result = isValid(s)
print(result)