
def countSwaps(a):
    swaps = 0
    i = 0
    while i < len(a):
        j = 0
        while j < len(a) - 1:
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
            j += 1
        i += 1

    return print((('Array is sorted in %d swaps.')% swaps + '\n' +
            ('First Element: %d') % min(a) + '\n' +
            ('Last Element: %d') % max(a)))

n = int(input())
a = list(map(int, input().rstrip().split()))
countSwaps(a)