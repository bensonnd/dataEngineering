#!/bin/python3

import math
import os
import random
import re
import sys



# Complete the maxMin function below.
def maxMin(k, arr):
    sortedarr = sorted(arr)
    minmaxlist = []
    for i in range(len(sortedarr) - k + 1):
        minmaxlist.append(sortedarr[i + k - 1] - sortedarr[i])

    return min(minmaxlist)

n = int(input())
k = int(input())
arr = []

for _ in range(n):
    arr_item = int(input())
    arr.append(arr_item)

result = maxMin(k, arr)
print(result)
