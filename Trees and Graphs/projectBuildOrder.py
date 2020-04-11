from collections import Counter


# build a dictionary with each project and counts its upline dependencies as well as list its downline dependencies
# {f: [0, ['a','b']], a: [1, ['d']], b: [1, ['d']], c: [1, []], d: [2, ['c']], e: [0, []]} -- {project: count of upline dependencies, [list of downline dependencies]...}

# TODO: Make this a class

def buildOrderdict(projects,dependencies):
    d = {key:[0,list()] for key in projects}
    for i in dependencies:
        dictKey = i[0]
        dependencyKey = i[1]
        d[dictKey][1].append(dependencyKey)
        d[dependencyKey][0] += 1
    return d

jobOrder = []

def buildOrder(jobDict: dict):
    try:
        for key,value in list(jobDict.items()):
            if len(jobDict) == 0:
                break
            if value[0] == 0:
                for i in value[1]:
                    jobDict[i][0] -= 1
                jobOrder.append(key)
                del jobDict[key]
                if len(jobDict) > 0:
                    buildOrder(jobDict)
    except KeyError:
        jobOrder.clear()
        return False
    return jobDict


projects = ['a','b','c','d','e','f','g']
dependencies = [('f','c'),('f','b'),('f','a'),('c','a'),('b','a'),('b','e'),('a','e'),('d','g')]

d = buildOrderdict(projects,dependencies)
buildOrder(d)
print(jobOrder)