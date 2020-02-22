from itertools import groupby

inputvar = input()

for key, group in groupby(inputvar, lambda x: x[0]):
    var_count = 0
    for num in group:
        var_count += 1
    print('(' + str(var_count) + ', ' + str(key) + ')', end = ' ')
