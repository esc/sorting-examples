from random import randint, shuffle, choice
from timeit import Timer
import numpy

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
    """ Stable out-of-place quicksort.

    Parameters
    ----------
    array : list
        a possibly unordered list
    Returns
    -------
    sorted : list
        a sorted list
    """
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
    """ Stable mergesort.

    Has the downside of popping items off of a list from the front, causing
    resizeing to happen all the time.

    Parameters
    ----------
    array : list
        a possibly unordered list
    Returns
    -------
    sorted : list
        a sorted list
    """
    if len(array) <= 1:
        return array
    part = len(array)//2
    return merge(mergesort(array[:part]), mergesort(array[part:]))

def merge(array1, array2):
    """ Helper for mergesort."""
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

def mergesort2(array):
    """ Stable mergesort.

    This implementation alleviates the problem of having to pop of the front of
    the list, but then needs to reverse it after each merge of two lists. Minor,
    but statistically significant speed up.

    Parameters
    ----------
    array : list
        a possibly unordered list
    Returns
    -------
    sorted : list
        a sorted list
    """
    if len(array) <= 1:
        return array
    part = len(array)//2
    return merge2(mergesort2(array[:part]), mergesort2(array[part:]))

def merge2(array1, array2):
    result = []
    while len(array1) or len(array2):
        # larger values go in first
        if len(array1) and len(array2):
            if array1[-1] >= array2[-1]:
                result.append(array1.pop())
            else:
                result.append(array2.pop())
        elif len(array1):
            result.append(array1.pop())
        else:
            result.append(array2.pop())
    # here we need to reverse the array, so that smaller values are at the
    # beginning
    # in numpy we could do this with strides, obviously
    # Still popping values of the end of the list and reversing is faster than
    # popping them off the front and resizing
    result.reverse()
    return result

def do_timing(timer):
    number=500
    print ("%.2f mseconds/pass" %
    (1000 * timer.timeit(number=number)/number))

array_size=256
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
    print 'Mergesort2'
    print array
    print mergesort2(array)

    shuffle(array)
    print 'Native'
    print array
    array.sort()
    print array

    a = numpy.arange(array_size)
    numpy.random.shuffle(a)
    print 'Numpy'
    print a
    a.sort()
    print a

def timing():

    print "Quicksort not-in-place"
    t = Timer("""
    array = range(%i)
    shuffle(array)
    quicksort_nip(array)
    """% array_size, "from __main__ import *" )
    do_timing(t)

    print "Quicksort in-place"
    t = Timer("""
    array = range(%i)
    shuffle(array)
    quicksort_ip(array, 0, len(array)-1)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Mergesort'
    t = Timer("""
    array = range(%i)
    shuffle(array)
    mergesort(array)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Mergesort2'
    t = Timer("""
    array = range(%i)
    shuffle(array)
    mergesort2(array)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Native'
    t = Timer("""
    array = range(%i)
    shuffle(array)
    array.sort()
    """% array_size, "from __main__ import *")
    do_timing(t)

    print 'Numpy'
    t = Timer("""
    a = numpy.arange(%i)
    numpy.random.shuffle(a)
    a.sort()
    """% array_size, "from __main__ import *")
    do_timing(t)

if __name__ == '__main__':
    timing()

#Quicksort not-in-place
#2.05 mseconds/pass
#Quicksort in-place
#2.97 mseconds/pass
#Mergesort
#3.94 mseconds/pass
#Mergesort2
#3.49 mseconds/pass
#Native
#0.38 mseconds/pass
#Numpy
#0.12 mseconds/pass
