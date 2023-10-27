# from memory_profiler import profile
# To keep track of the memory profiler for each sorting method
import random
import timeit


# @profile
def insertion_sort(input_array):
    array_size = len(input_array)
    for i in range(1, array_size):
        # Go through each element of the array
        key = input_array[i]
        j = i - 1
        while j >= 0 and key < input_array[j]:
            # Move elements which are greater than above selected key, to one position ahead of their current position
            input_array[j + 1] = input_array[j]
            j -= 1
        input_array[j + 1] = key
    return input_array


# @profile
def merge_sort(array):
    if len(array) > 1:
        mid = len(array) // 2
        # To find the middle element of the given array
        left = array[:mid]
        # Dividing array in to 2 parts by middle element of the array
        right = array[mid:]
        merge_sort(left)
        # Sorting the left half
        merge_sort(right)
        # Sorting the right half
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            # Copy data to temp array from left half and right half
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1
        while (i < len(left)):
            # Check whether if any element is remaining in left half
            array[k] = left[i]
            i += 1
            k += 1
        while (j < len(right)):
            # Check whether if any element is remaining in right half
            array[k] = right[j]
            j += 1
            k += 1

        return array


def insertion_sort_helper_for_tim_sort(input_array, start, end):
    array_size = len(input_array)
    for i in range(start + 1, end + 1):
        # Go through each element of the array
        key = input_array[i]
        j = i - 1
        while j >= start and input_array[j] > key:
            # Move elements which are greater than above selected key, to one position ahead of their current position
            input_array[j + 1] = input_array[j]
            j -= 1
        input_array[j + 1] = key


def merge(input_array, l, m, r):
    len1 = m + 1 - l
    len2 = r - m

    left = []
    right = []
    for i in range(len1):
        left.append(input_array[l + i])
    for j in range(len2):
        right.append(input_array[m + 1 + j])

    i = 0
    j = 0
    k = l

    while i < len1 and j < len2:
        if left[i] <= right[j]:
            input_array[k] = left[i]
            i += 1
        else:
            input_array[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        input_array[k] = left[i]
        i += 1
        k += 1

    while j < len2:
        input_array[k] = right[j]
        j += 1
        k += 1


# @profile
def tim_sort(input_array):
    min_run = 32

    for i in range(0, len(input_array), min_run):
        insertion_sort_helper_for_tim_sort(input_array, i, min((i + min_run - 1), len(input_array) - 1))

    size = min_run
    while size < len(input_array):
        for start in range(0, len(input_array), size * 2):
            mid = min((start + size - 1), (len(input_array) - 1))
            end = min((start + size * 2 - 1), (len(input_array) - 1))

            if mid < end:
                merge(input_array, start, mid, end)

        size *= 2
    return input_array


def generate_data(size, scenario):
    """
    Method to generate test data for different scenarios
    """
    if scenario == "random":
        return [random.randint(1, size) for _ in range(size)]
    if scenario == "nearly_sorted":
        data = list(range(1, size + 1))
        # Shuffle a small portion of data
        for i in range(size // 10):
            j, k = random.randint(0, size - 1), random.randint(0, size - 1)
            data[j], data[k] = data[k], data[j]
        return data
    if scenario == "inversely_sorted":
        return list(range(size, 0, -1))


# Benchmark function
def benchmark_algorithm(sort_func, data, scenario):
    setup = f"from __main__ import {sort_func}, generate_data, data"
    stmt = f"{sort_func}(data)"
    time_taken = timeit.timeit(stmt, setup, number=10)

    expected_result = sorted(data.copy())

    print(f"{sort_func} ({scenario} data): {time_taken:.6f} seconds")


if __name__ == "__main__":
    data_sizes = [100]  # Add data sizes as needed to compare
    scenarios = ["random", "nearly_sorted", "inversely_sorted"]
    sorting_algorithms = [insertion_sort, merge_sort, tim_sort]

    for size in data_sizes:
        for scenario in scenarios:
            data = generate_data(size, scenario)
            for sort_func in sorting_algorithms:
                benchmark_algorithm(sort_func.__name__, data.copy(), scenario)
            print()
            # Add a newline between different data scenarios
