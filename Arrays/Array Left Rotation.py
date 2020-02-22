# Complete the rotLeft function below.
def rotLeft(a, d):
    for rotations in range(d):
        list_end = a[0]
        a.pop(0)
        a.append(list_end)
    return a

