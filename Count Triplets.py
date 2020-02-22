#!/bin/python3
from itertools import groupby
from functools import reduce

import math
import os
import random
import re
import sys
from collections import Counter

def counttripletcounters(arr, r):
    # doubletcounter - counting potential doublet end numbers - where num in arr is left side of doublet,
    # if num 1 in arr, potential future doublet would be (1,2), and with 2, (2,4), and so on...
    doubletcounter = Counter()
    #tripletcounter - counting potential triplet end numbers - if num in arr is end of doublet, multiply by r, and count as a potential
    #triplet - if num in arr is 2, and is end of doublet, add 2 * r as potential right side of triplet
    tripletcounter = Counter()
    count = 0

    for num in arr:
        if num in tripletcounter:
            #increment counter where num matches end of tripletcounter and is also end of doubletcounter
            count += tripletcounter[num]

        if num in doubletcounter:
            # increment tripletcounter where num matches end of doublet, for future potential numbers to match end of triplet
            testcount = doubletcounter[num]
            tripletcounter[num * r] += testcount

        #num to doubletcounter for future potential numbers to match end of doublet
        doubletcounter[num * r] += 1

    return count

#arr[0]*r^(5-1)

nr = input().rstrip().split()
n = int(nr[0])
r = int(nr[1])
arr = list(map(int, input().rstrip().split()))
print(arr)
ans = counttripletcounters(arr, r)
print(ans)
