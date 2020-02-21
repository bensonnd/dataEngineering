from itertools import groupby

def groupingList(list):
    groupbylist = []
    for key, group in groupby(list, lambda x: x):
        var_count = 0
        for num in group:
            var_count += 1
        groupbylist.append([var_count, key])
    return groupbylist

def freqQuery(queries):
    query_list = []
    return_list = []
    for iind, i in enumerate(queries):
        if i[0] == 1: query_list.append(i[1])
        elif i[0] == 2 and i[0] in query_list:
            query_list.remove(i[1])
        elif i[0] == 3:
            check_ist = [j for j in groupingList(sorted(query_list)) if j[0] == i[1]]
            if len(check_ist) > 0: return_list.append(1)
            else: return_list.append(0)
    return return_list



q = int(input().strip())
queries = []
for _ in range(q):
    queries.append(list(map(int, input().rstrip().split())))

inserts = [i for i in queries if i[0] == 1]
insert_nums = [i[1] for i in inserts]
deletes = [i for i in queries if i[0] == 2]
delete_nums = [i[1] for i in deletes]
missing_nums = [i for i in delete_nums if i not in insert_nums]
print(missing_nums)
ans = freqQuery(queries)
#print(queries)
print(ans)