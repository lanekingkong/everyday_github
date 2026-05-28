"""
Sorting Algorithm Visualizer — Terminal Edition
Shows bubble, selection, insertion, merge, quick sort step-by-step.
"""
import time
import random
import os


def bubble_sort(arr, steps_callback=None):
    n = len(arr)
    steps = 0
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            steps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                if steps_callback:
                    steps_callback(arr, j, j + 1, "Bubble")
        if not swapped:
            break
    return steps


def selection_sort(arr, steps_callback=None):
    n = len(arr)
    steps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if steps_callback:
            steps_callback(arr, i, min_idx, "Selection")
    return steps


def insertion_sort(arr, steps_callback=None):
    steps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            steps += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        if steps_callback:
            steps_callback(arr, j + 1, i, "Insertion")
    return steps


def merge_sort(arr, steps_callback=None):
    steps = [0]

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            steps[0] += 1
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _sort(a[:mid])
        right = _sort(a[mid:])
        merged = _merge(left, right)
        if steps_callback:
            steps_callback(merged, -1, -1, "Merge")
        return merged

    result = _sort(arr.copy())
    arr[:] = result
    return steps[0]


def display_step(arr, i, j, algo_name):
    """Print array with highlighted positions."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"═══ {algo_name} Sort ═══")
    print()
    bar = ""
    for idx, val in enumerate(arr):
        c = "█" if idx in (i, j) else "░"
        bar += c * max(1, val // 2) + f" {val}\n"
    print(bar)
    time.sleep(0.05)


def benchmark():
    sizes = [100, 500, 1000, 2000]
    algorithms = {
        "Bubble": bubble_sort,
        "Selection": selection_sort,
        "Insertion": insertion_sort,
        "Merge": merge_sort,
    }
    print("\n═══ Benchmark (ops count) ═══\n")
    print(f"{'Size':>8}", end="")
    for name in algorithms:
        print(f"{name:>12}", end="")
    print()
    print("-" * 56)

    for size in sizes:
        print(f"{size:>8}", end="")
        for name, algo in algorithms.items():
            arr = list(range(size, 0, -1))
            ops = algo(arr)
            print(f"{ops:>12}", end="")
        print()
    print()


if __name__ == "__main__":
    print("\n🧮 Sorting Algorithm Visualizer\n")

    # Demo with visualization
    arr = [random.randint(1, 50) for _ in range(25)]
    print("Original:", arr)
    print("\nRunning Bubble Sort with visualization...\n")
    time.sleep(1)

    demo = arr.copy()
    bubble_sort(demo, display_step)

    print("\nSorted:", demo)
    print(f"\n✅ Correct: {demo == sorted(arr)}")

    benchmark()
