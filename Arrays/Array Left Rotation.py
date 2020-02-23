# Complete the rotLeft function below.
def rotLeft(a, d):
    remainder = d % len(a)
    divisions = d // len(a)
    reduced_rotations = remainder + divisions
    list_end = a[:reduced_rotations - len(a)]
    del a[:reduced_rotations - len(a)]
    a = a + list_end
    return a

def getMaxElementIndexes(a, rotate):
    maxindexlist = []
    for i in rotate:
        templist = a.copy()
        if i == 0:
            maxindexlist.append(templist.index(max(templist)))
        else:
            rotate_list = rotLeft(templist,i)
            maxindexlist.append(templist.index(max(rotate_list)))
    return maxindexlist



a = [1,2,3,4,5]
rotate = [1,0,37]
result = getMaxElementIndexes(a, rotate)
print(result)