#!/bin/python3
from itertools import groupby

# Complete the makeAnagram function below.
def groupingList(list):
    groupbylist = []
    for key, group in groupby(list, lambda x: x[0]):
        var_count = 0
        for num in group:
            var_count += 1
        groupbylist.append([var_count, key])
    return groupbylist

def makeAnagram(a, b):
    delete_charsa = [i for i in a if i not in b]            #find all the values not in a
    delete_charsb = [i for i in b if i not in a]            #find all the values not in a
    keep_charsa_count = groupingList(str(''.join(sorted([i for i in a if i not in delete_charsa]))))    #create list of counts of each letter remaining in a
    keep_charsb_count = groupingList(str(''.join(sorted([i for i in b if i not in delete_charsb]))))    #create list of counts of each letter remaining in b
    delete_count = 0
    for iind, i in enumerate(keep_charsa_count):
        delete_count += abs(keep_charsa_count[iind][0] - keep_charsb_count[iind][0])

    return  delete_count + len(delete_charsa) + len(delete_charsb)

    #return delete_charsa, delete_charsb, ''.join(sorted(keep_charsa)), ''.join(sorted(keep_charsb)), (len(delete_charsa) + len(delete_charsb)) + (maxlengthkeep - lengthUnique), maxlengthkeep, lengthUnique, len(delete_charsa), len(delete_charsb), ''.join(sorted(set(str(''.join(sorted(keep_charsa))) + str(''.join(sorted(keep_charsb))))))

a = 'bugexikjevtubidpulaelsbcqlupwetzyzdvjphn'
b = 'lajoipfecfinxjspxmevqxuqyalhrsxcvgsdxxkacspbchrbvvwnvsdtsrdk'

res = makeAnagram(a, b)
print(res)
