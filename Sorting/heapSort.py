def left(indx):
    return int(2 * indx)            # set the index of the left child

def right(indx):
    return int(2 * indx + 1)        # set the index of the right child

def maxHeapify (arr, indx):
    '''
    This functions creates a binary tree of parent and two children nodes. Each parent is larger than any of its children.
    The function crawls down the tree moving the higher values up.
    The parent node and left and right children are normalized to array starting at 0. In recursion, the subtracted 1 is added
    back in so function can keep craling down, and moving larger values up.
    :param arr the array to max heapify
    :param indx the parent node to evaulate
    :return a heapified array. ex. [4, 3, 1, 5, 2, 7, 6] --> [7, 5, 6, 3, 2, 1, 4]
    '''
    parentnode = indx - 1                               # normalize parentnode to array index of 0
    l = left(indx) - 1                                  # returns the index of the left child of the current parent, ie. index = 0, left = 1, or index = 1, left = 3
    r = right(indx) -1                                  # returns the index of the right child of the current parent, ie. index = 0, right = 2, or index = 2, right = 6
    heapsize = len(arr)

    if l < heapsize and arr[l] > arr[parentnode]:      # check to see if left child is bigger than parent, if so set largest to l
        largest = l
    else:
        largest = parentnode                           # if parentnode is bigger set largest to parentnode
    if r < heapsize and arr[r] > arr[largest]:         # check to see if right child is bigger than parent or left child, if so set largest to r
        largest = r
    if largest != parentnode:                                           # move largest from child to parent
        arr[parentnode], arr[largest] = arr[largest], arr[parentnode]
        maxHeapify(arr,largest + 1)                     #add 1 to account for subtracting 1 at beginning of function
    return arr

def buildMaxHeap(arr):
    heapsize = len(arr)
    i = heapsize//2         # start the with lowest level of parent nodes with children
    while i > 0:
        maxHeapify(arr,i)
        i -= 1

def heapSort(arr):
    '''Takes an array, builds a max heap out of it, moves the 0 index/MAX value to the end, and heapifies each remaining element.
    :param arr: the array to sort
    :return: a sorted array
    '''
    buildMaxHeap(arr)
    heapsize = len(arr)
    for i in reversed(range(2,heapsize)):
        arr[0], arr[i] = arr[i], arr[0]     #move max value in heapified array to end
        heapsize -= 1                       #exclude max value at end of heapified array in next heapification
        b = 2
        maxHeapify(arr[:heapsize],1)        #TODO check to see how to perform a function/manipulation on list slice in place - not bringing in the heapified list to the existing array
`
    return arr

array = [23,17,14,6,13,10,1,5,7,12]
print(array)
print(heapSort(array))

