"""
Additional sorting algorithms for the visualizer.
Includes: quick sort, heap sort, shell sort.
"""


def quick_sort(arr, low=0, high=None):
    """In-place quick sort with Lomuto partition."""
    if high is None:
        high = len(arr) - 1
    ops = [0]

    def _partition(lo, hi):
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            ops[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    def _sort(lo, hi):
        if lo < hi:
            p = _partition(lo, hi)
            _sort(lo, p - 1)
            _sort(p + 1, hi)

    _sort(low, high)
    return ops[0]


def heap_sort(arr):
    """Heap sort using max-heap."""
    n = len(arr)
    ops = [0]

    def _heapify(size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size:
            ops[0] += 1
            if arr[left] > arr[largest]:
                largest = left
        if right < size:
            ops[0] += 1
            if arr[right] > arr[largest]:
                largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            _heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(i, 0)
    return ops[0]


def shell_sort(arr):
    """Shell sort with gap sequence."""
    n = len(arr)
    ops = [0]
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap:
                ops[0] += 1
                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                else:
                    break
            arr[j] = temp
        gap //= 2
    return ops[0]
