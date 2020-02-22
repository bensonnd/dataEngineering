# Complete the hourglassSum function below.
def hourglassSum(arr):
    max_list = []
    for iind, i in enumerate(arr[:4]):
        for jind, j in enumerate(i):
            if iind <= 3 and jind <= 3:
                hourglasswhole = []
                hourglasstop = i[jind:jind+3]
                hourglassmiddle = [arr[iind+1][jind+1]]
                hourglassbottom = arr[iind+2][jind:jind+3]
                hourglasswhole.append(list(hourglasstop))
                hourglasswhole.append(list(hourglassmiddle))
                hourglasswhole.append(list(hourglassbottom))
                sumhourglass = sum(hourglasstop + hourglassmiddle + hourglassbottom)
                max_list.append(sumhourglass)

    return max(max_list)