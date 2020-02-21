# Complete the twoStrings function below.
def twoStrings(s1, s2):
    countsubstr = [i for i in s1 if i in s2]
    if len(countsubstr) >= 1: return 'YES'
    else: return 'NO'


q = int(input())

for q_itr in range(q):
    s1 = input()
    s2 = input()
    result = twoStrings(s1, s2)
    print(result)