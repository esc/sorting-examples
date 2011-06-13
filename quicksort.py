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
    if low >= high:
        return
    part = randint(low, high)
    swap(array, part, low)
    counter = low
    for i in range(low+1, high+1):
        if array[i] < array[low]:
            counter+=1
            swap(array, counter, i)
    swap(array, low, counter)
    quicksort(array, low, counter-1)
    quicksort(array, counter+1, high)

array = range(0, 32)
shuffle(array)
print array
quicksort(array, 0, len(array)-1)
print array
