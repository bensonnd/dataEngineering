from collections import Counter
from numpy import gcd

def letterCount(text):
    return Counter(c for c in text.lower() if c.isalpha())

def findSmallestDivisor(s, t):
    """
    This functions checks to see if a string s is divisible by t. A string is divisible if t exists in s 1 or more times, and s only consists of multiples of t
    examples:
        s = "rbrb", t = "rb" - is divisible, returns unique len of t "rb" is (2)
        s = "llrb" , t = "llrb" - is divisible, returns unique len of t "llrb" is (4)
        s = "xxrrbbxxrrbb" , t = "xxrrbb" - is divisible, returns unique len of t "xxrrbb" is (6)
        s = "llrbe" , t = "llrb" - not divisible, returns unique -1
    :param s: the string to divide/the numerator
    :param t: the string to divide by/the denominator
    :return: the length unique of the denominator t, if s is divisible by t
    """
    numDict, denDict = letterCount(s), letterCount(t)   # keep track of the count of letters in both strings, the denominator and numerator
    greatComNum, greatComDen,  = gcd.reduce(list(set(numDict.values()))), gcd.reduce(list(set(denDict.values()))) # get each dictionaries greatest common denominator for count of letters
    sumNumVals, sumDenVals = int(sum(numDict.values())), int(sum(denDict.values())) # get the sum total count of all letters in each dictionary
    # if they aren't the same length, they can't be divided by each other
    if len(numDict) != len(denDict):
        return -1
    # check to see that the count in s is divisible by count in t
    for key in numDict:
        if numDict[key] % denDict[key] == 0: continue
        else:
            return -1
    # if there is only letter in s and t, count the length (1)
    if len(denDict) == 1:
        return len(denDict)
    # if all the letters have the same count, sum them together and divide by total length of dict for uniqueness
    elif len(set(denDict.values())) == 1:
        return int(round(sumDenVals/len(denDict)))

    elif sumDenVals/greatComDen != sumNumVals/greatComNum:
        return -1
    # divide the total count of letters in t by greatest common denominator for uniqueness
    else:
        return int(round(sumDenVals/greatComDen))

s = 'llrb'
t = 'llrb'

# print(letterCount(s))
# print(letterCount(t))
print(findSmallestDivisor(s, t))

