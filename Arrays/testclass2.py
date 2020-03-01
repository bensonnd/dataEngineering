def add10tolist(li):
    listtoreturn = []
    for i in range(len(li)):
        listtoreturn.append(li[i] + 10)
    return listtoreturn

#or
def add10tolist(li):
    nl = [x + 10 for x in li]
    return nl


li = [20, 30, 50, 10, 15, 35]

print(add10tolist(li))