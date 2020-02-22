# Complete the twoStrings function below.
def twoStrings(s1, s2):
    countsubstr = [i for i in s1 if i in s2]
    if len(countsubstr) >= 1: return 'YES'
    else: return 'NO'