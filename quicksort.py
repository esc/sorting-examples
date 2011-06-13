from random import randint, shuffle

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]

def quicksort(array, low, high):
    """ Sort 'array' in place.
    Parameters
    ----------
    low : int
        smallest index to consider
    high : int
        largest index to consider
    """
    print 'start-------------------'
    if low >= high:
        print 'recursion base case'
        return
    print 'sorting', array[low:high+1]
    part = randint(low, high)
    print 'part', part
    swap(array, part, low)
    print 'swapped', array[low:high+1]
    counter = low
    for i in range(low+1, high+1):
        print i
        if array[i] < array[low]:
            counter+=1
            print 'swapping', counter, i
            swap(array, counter, i)
    print 'counter', counter
    print 'b4-swap-back', array[low:high+1]
    swap(array, low, counter)
    print 'swapped-back', array[low:high+1]
    print 'end----------------------'
    quicksort(array, low, counter-1)
    quicksort(array, counter+1, high)

array = range(0, 32)
shuffle(array)
print array
quicksort(array, 0, len(array)-1)
print array
