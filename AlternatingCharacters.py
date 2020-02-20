from itertools import groupby

#counts the number of repeitive letters ex. AABA = [[1,A],[2,A],[1,B],[1,A]] or AAAA = [[1,A],[2,B],[3,A],[4,A]
def groupingList(list):
    groupbylist = []
    for key, group in groupby(list, lambda x: x[0]):
        var_count = 0
        for num in group:
            var_count += 1
            groupbylist.append([var_count, key])
    return groupbylist

# Complete the alternatingCharacters function below.
def alternatingCharacters(s):
    grou_chars_count = groupingList(str(''.join([i for i in s]))) #count each letter in repetition
    return len([i for i in grou_chars_count if i[0] > 1]) #remove single instance of letter and count remaining list items

q = int(input())
for q_itr in range(q):
    s = input()
    result = alternatingCharacters(s)
    print(result)