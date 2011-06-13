from random import randint, shuffle, choice
from timeit import Timer

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]

def quicksort_ip(array, low, high):
    """ Sort 'array' in place.
    Parameters
    ----------
    low : int
        smallest index to consider
    high : int
        largest index to consider
    """
    if low >= high:
        return
    part, counter = randint(low, high), low
    swap(array, part, low)
    for i in range(low+1, high+1):
        if array[i] < array[low]:
            counter+=1
            swap(array, counter, i)
    swap(array, low, counter)
    quicksort_ip(array, low, counter-1)
    quicksort_ip(array, counter+1, high)

def quicksort_nip(array):
    """ Stable out-of-place quicksort."""
    if len(array) <= 1:
        return array
    lower, upper, center = [], [], []
    part = choice(array)
    for i in array:
        if i < part:
            lower.append(i)
        elif i > part:
            upper.append(i)
        else:
            center.append(i)
    return quicksort_nip(lower) + center + quicksort_nip(upper)

def mergesort(array):
    if len(array) <= 1:
        return array
    part = len(array)//2
    return merge(mergesort(array[:part]), mergesort(array[part:]))

def merge(array1, array2):
    result = []
    while len(array1) or len(array2):
        if len(array1) and len(array2):
            if array1[0] <= array2[0]:
                result.append(array1.pop(0))
            else:
                result.append(array2.pop(0))
        elif len(array1):
            result.append(array1.pop(0))
        else:
            result.append(array2.pop(0))
    return result

def do_timing(timer):
    number=500
    print ("%.2f usec/pass" %
    (number * timer.timeit(number=number)/number))

array_size=1024
array = range(array_size)

def testing():

    shuffle(array)
    print "Quicksort not-in-place"
    print array
    print quicksort_nip(array)

    shuffle(array)
    print "Quicksort in-place"
    print array
    quicksort_ip(array, 0, len(array)-1)
    print array

    shuffle(array)
    print 'Mergesort'
    print array
    print mergesort(array)

    shuffle(array)
    print 'Native'
    print array
    array.sort()
    print array

def timing():

    print "Quicksort not-in-place"
    t = Timer("""
    array = range(0, %i)
    shuffle(array)
    quicksort_nip(array)
    """% array_size, "from __main__ import *" )
    do_timing(t)

    print "Quicksort in-place"
    t = Timer("""
    array = range(0, %i)
    shuffle(array)
    quicksort_ip(array, 0, len(array)-1)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Mergesort'
    t = Timer("""
    array = range(0, %i)
    shuffle(array)
    mergesort(array)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Native'
    t = Timer("""
    array = range(0, %i)
    shuffle(array)
    array.sort()
    """% array_size, "from __main__ import *")
    do_timing(t)
if __name__ == '__main__':
    timing()
