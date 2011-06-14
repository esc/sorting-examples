from random import randint, shuffle, choice, randrange
from timeit import Timer
import numpy
import numpy.testing
import nose.tools as nt

def quicksort_val(array):
    """ Stable out-of-place quicksort.

    This is written by yours truely in pythonic style.

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
    return quicksort_val(lower) + center + quicksort_val(upper)

def swap(array, i, j):
    """ Helper function for quicksort_ip. """
    array[i], array[j] = array[j], array[i]

def quicksort_ip(array, low, high):
    """ Sort 'array' in place.

    This is converted from C code found in chapter three of:
    Beautiful Code
    Leading Programmers Explain How They Think

    Edited By Andy Oram & Greg Wilson
    First Edition Juli 2007
    ISBN 978-0-596-51004-6

    Should be fast as hell, no idea why its so slow.

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
    for i in xrange(low+1, high+1):
        if array[i] < array[low]:
            counter+=1
            swap(array, counter, i)
    swap(array, low, counter)
    quicksort_ip(array, low, counter-1)
    quicksort_ip(array, counter+1, high)


def quicksort_lc(array):
    """ This is a quicksort using list comprehensions.

    It is taken from:
        http://en.literateprograms.org/Quicksort_(Python)
    According to the article it was the fastest of all of the three. However it
    doesn't run faster than val's quicksort. Perhaps this is due to having to
    iterate over the array twice each time, for each list comprehension?

    Parameters
    ----------
    array : list
        a possibly unordered list
    Returns
    -------
    sorted : list
        a sorted list
    """
    if array == []: 
        return []
    else:
        pivot = array.pop(randrange(len(array)))
        lesser = quicksort_lc([l for l in array if l < pivot])
        greater = quicksort_lc([l for l in array if l >= pivot])
        return lesser + [pivot] + greater


def mergesort(array):
    """ Stable mergesort.

    Written by yours truly but inspired by pseudocode from:
        http://en.wikipedia.org/wiki/Merge_sort

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
    """ Stable mergesort (second version).

    An improvement on mergesort.

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
    """ Helper for mergesort2."""
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

def mergesort3(array):
    """ Stable mergesort.

    The code was taken from:
        http://en.literateprograms.org/Merge_sort_(Python)

    This one uses indices instead of popping from the list. Also the
    merge-helper is nicer. But code is less pythonic (uses indices). Faster than
    the previous two implementations.

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
    return merge3(mergesort3(array[:part]), mergesort3(array[part:]))

def merge3(array1, array2):
    """ Helper for mergesort2."""
    result = []
    i,j = 0,0
    while i < len(array1) and j < len(array2):
        if array1[i] <= array2[j]:
            result.append(array1[i])
            i+=1
        else:
            result.append(array2[j])
            j+=1
    result += array1[i:]
    result += array2[j:]
    return result

number=10
array_size=50000
def do_timing(timer):
    print ("%.2f mseconds/pass" %
    (1000 * timer.timeit(number=number)/number))

array = range(array_size)
original=array[:]

def testing():

    print 'Testing'
    print "-----------------------------------------------------------"

    shuffle(array)
    print "Quicksort not-in-place"
    nt.assert_equal(quicksort_val(array),original)

    shuffle(array)
    print "Quicksort in-place"
    quicksort_ip(array, 0, len(array)-1)
    nt.assert_equal(array,original)

    shuffle(array)
    print "Quicksort list comprehension"
    to_sort = array[:]
    nt.assert_equal(quicksort_lc(to_sort), original)

    shuffle(array)
    print 'Mergesort'
    nt.assert_equal(mergesort(array),original)

    shuffle(array)
    print 'Mergesort2'
    nt.assert_equal(mergesort2(array),original)

    shuffle(array)
    print 'Mergesort3'
    nt.assert_equal(mergesort3(array),original)

    shuffle(array)
    print 'Native'
    array.sort()
    nt.assert_equal(array,original)

    a = numpy.arange(array_size)
    o = a.copy()
    numpy.random.shuffle(a)
    print 'Numpy'
    a.sort()
    numpy.testing.assert_array_equal(a,o)

    print "-----------------------------------------------------------"

def timing():

    print 'Timing'
    print "-----------------------------------------------------------"

    print "Quicksort not-in-place"
    t = Timer("""
    array = range(%i)
    shuffle(array)
    quicksort_val(array)
    """% array_size, "from __main__ import *" )
    do_timing(t)

    print "Quicksort in-place"
    t = Timer("""
    array = range(%i)
    shuffle(array)
    quicksort_ip(array, 0, len(array)-1)
    """% array_size, "from __main__ import *")
    do_timing(t)

    print "Quicksort list comprehension"
    t = Timer("""
    array = range(%i)
    shuffle(array)
    quicksort_lc(array[:])
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

    print 'Mergesort3'
    t = Timer("""
    array = range(%i)
    shuffle(array)
    mergesort3(array)
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

    print "-----------------------------------------------------------"

if __name__ == '__main__':
    testing()
    timing()

#Quicksort not-in-place
#2.05 mseconds/pass
#Quicksort in-place
#2.97 mseconds/pass
#Mergesort
#3.94 mseconds/pass
#Mergesort2
#3.49 mseconds/pass
#Mergesort3
#1.17 mseconds/pass
#Native
#0.38 mseconds/pass
#Numpy
#0.12 mseconds/pass
