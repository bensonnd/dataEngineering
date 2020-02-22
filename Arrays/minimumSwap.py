#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the minimumSwaps function below.
def minimumSwaps(arr):
    arrmin = min(arr)
    temparr = [i - arrmin + 1 for i in arr]     #normalize the list to start at 1
    temp = temparr.copy()
    for iind, a in enumerate(temparr):
        temp[a - 1] = iind                      #give temparr an index for each value
    swaps = 0
    for i in range(len(temparr) - 1):
        a = temparr[i]
        if a != i + 1:
            swaps += 1
            temparr[i] = i + 1
            temparr[temp[i]] = a
            temp[a - 1] = temp[i]
    return print((('Array is sorted in %d swaps.')% swaps + '\n' +
            ('First Element: %d') % min(arr) + '\n' +
            ('Last Element: %d') % max(arr)))



n = int(input())
a = list(map(int, input().rstrip().split()))
minimumSwaps(a)