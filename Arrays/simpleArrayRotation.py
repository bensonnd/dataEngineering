def getMaxElementIndexes(li, rotatelist):
    '''Returns the index of the max of the list after "rotating" the number of times in the rotation list.
    This function does not physically move each element in the list per rotation, rather keeps track of a list's
    index positions and how many times it should move and to where.'''
    maxindexlist = [] # keep track of the indexes of the list after "rotation"
    maxIndex = li.index(max(li)) #get the index of the max value before rotations
    for i in rotatelist: #iterate through all the rotations
        if i == 0:  #if roations are zero append the current index of the max value
            maxindexlist.append(maxIndex)
        else:
            remainder = i % len(li) #find how many spots the max has to move
            finalposition = maxIndex - remainder #"move" the max from its current position to its new position
            if finalposition < 0: #if that new position rolls around to the end of the list subtract final position from length
                maxindexlist.append(len(li) + finalposition)
            else:
                maxindexlist.append(finalposition) #else return the new position of the max after it has "moved"
    return maxindexlist

a = [0,1,2,3,70,5,6,7,8,9,10,11,12]
rotate = [2,13,14,15,6,7,100,1000000000,1000000001]
result = getMaxElementIndexes(a, rotate)
print(result)
