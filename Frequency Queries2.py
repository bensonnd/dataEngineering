import collections

def freqQuery(queries):
    freq = collections.Counter()
    cnt = collections.Counter()
    arr = []

    for q in queries:
        if q[0] == 1:
            cnt[freq[q[1]]] -= 1
            freq[q[1]] += 1
            cnt[freq[q[1]]] += 1

        elif q[0] == 2:
            if freq[q[1]] > 0:
                cnt[freq[q[1]]] -= 1
                freq[q[1]] -= 1
                cnt[freq[q[1]]] += 1

        else:
            if cnt[q[1]] > 0:
                arr.append(1)
            else:
                arr.append(0)

    return arr


q = int(input().strip())
queries = []
for _ in range(q):
    queries.append(list(map(int, input().rstrip().split())))

#inserts = [i for i in queries if i[0] == 1]
#insert_nums = [i[1] for i in inserts]
#deletes = [i for i in queries if i[0] == 2]
#delete_nums = [i[1] for i in deletes]
#missing_nums = [i for i in delete_nums if i not in insert_nums]
#print(missing_nums)
ans = freqQuery(queries)
#print(queries)
print(ans)