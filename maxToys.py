# Complete the maximumToys function below.
from itertools import accumulate

def maximumToys(prices, k):
    # drop any toys that over the total budget price
    prices_list = [i for i in prices if i <= k]
    #check to see if sum of remaining toys are under total budget
    if sum(prices_list) <= k: return len(prices_list)
    else:
        #sort and keep running total of toy prices
        toypricestotal = list(accumulate(sorted(prices_list)))
        #drop all list items where cumulative total is greater than k
        new_prices_list = [i for i in toypricestotal if i <= k]
        return len(new_prices_list)


nk = input().split()
n = int(nk[0])
k = int(nk[1])
prices = list(map(int, input().rstrip().split()))
result = maximumToys(prices, k)
print(result)