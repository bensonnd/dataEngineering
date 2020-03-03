def left(indx):
    return int(2 * indx)

def right(indx):
    return int(2 * indx + 1)

def maxHeapify (arr, indx):
    l = left(indx) - 1 #returns the left of the current index, ie. index = 0, left = 1, or index = 1, left = 3
    r = right(indx) -1 #returns the right of the current index, ie. index = 0, right = 2, or index = 2, right = 6
    adjustedind = indx - 1
    heapsize = len(arr)
     if l <= heapsize and arr[l] > arr[adjustedind]:
        largest = l
    else:
        largest = adjustedind
    if r <= heapsize and arr[r] > arr[adjustedind]:
        largest = r
    if largest != adjustedind:
        arr[adjustedind], arr[largest] = arr[largest], arr[adjustedind]
        maxHeapify(arr,largest)

def buildMaxHeap(arr):
    heapsize = len(arr)
    i = heapsize//2
    while i >= 0:
        maxHeapify(arr,i)
        print(arr)
        i -= 1

def heapSort(arr):
    buildMaxHeap(arr)

    return arr

array = [4,3,1,5,2,7,6]

print(heapSort(array))
