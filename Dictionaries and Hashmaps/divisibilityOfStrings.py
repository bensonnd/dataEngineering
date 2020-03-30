from collections import Counter
from numpy import gcd

def letterCount(text):
    return Counter(c for c in text.lower() if c.isalpha())

def findSmallestDivisor(s, t):
    numDict, denDict = letterCount(s), letterCount(t)
    greatComNum, greatComDen,  = gcd.reduce(list(set(numDict.values()))), gcd.reduce(list(set(denDict.values())))
    sumNumVals, sumDenVals = int(sum(numDict.values())), int(sum(denDict.values()))
    if len(numDict) != len(denDict):
        return -1
    for key in numDict:
        if numDict[key] % denDict[key] == 0: continue
        else:
            return -1
    if len(denDict) == 1:
        return len(denDict)
    elif len(set(denDict.values())) == 1:
        return int(round(sumDenVals/len(denDict)))
    elif sumDenVals/greatComDen != sumNumVals/greatComNum:
        return -1
    else:
        return int(round(sumDenVals/greatComDen))

s = 'llrb'
t = 'llrb'

# print(letterCount(s))
# print(letterCount(t))
print(findSmallestDivisor(s, t))

