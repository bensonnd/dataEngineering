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
    return arr

def heapSort(arr):
    '''Takes an array, builds a max heap out of it, moves the 0 index/MAX value to the end, and heapifies each remaining element.
    :param arr: the array to sort
    :return: a sorted array
    '''
    buildMaxHeap(arr)
    heapsize = len(arr)
    #sort the heap
    for i in reversed(range(1, heapsize)):
        arr[0], arr[i] = arr[i], arr[0]  # move max value in heapified array to end
        heapsize -= 1  # exclude max value at end of heapified array in next heapification
        arr[:heapsize] = maxHeapify(arr[:heapsize],
                                    1)  # re-heap each new slice of the array as the heap decreases in size
    return arr

def heapIncreaseKey(arr, i, key):
    # parent = (i - 1) // 2
    if key < arr[i]:
        print("Err - New key is smaller than current key")
    arr[i] = key
    buildMaxHeap(arr)
    return arr

def maxHeapInsert(key, arr=[]):
    arr.append(float("-inf"))
    heapsize = len(arr) - 1
    heapIncreaseKey(arr, heapsize, key)
    return arr

def heapMax (arr):
    return arr[0]

array = [17,14,6,23,13,10,1,5,7,12,89,90,7434,22]
print(array)
print(buildMaxHeap(array))
print(maxHeapInsert(27,array))
print(heapSort(array))

gen_exp = (min(array[i:i+3]) for i in range(len(array) - 2)) # generator to iterate over the list, get the min for every 3 elements
listicle = []
for i in gen_exp:
   maxHeapInsert(i, listicle) # doesn't iterate over the list until it's called here, so it only traverses the list once

print(listicle)
print(heapMax(listicle))



