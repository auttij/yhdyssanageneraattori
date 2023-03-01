from itertools import product
from time import perf_counter

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return [i.strip() for i in f.readlines()]
    
def append_to_file(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        for line in data:
            f.write(f"{line}\n")

def binary_search(arr, check_function):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if check_function(arr[m]) > 0:
            lo = m + 1
        elif check_function(arr[m]) < 0:
            hi = m - 1
        else:
            return m
    return -1

def make_combinations(base, a, b):
    l = len(base)
    # for (i, j) in product(b, a):
    #     print(f"{i}{j[l:]}", i, j)
    return (f"{i}{j[l:]}" for (i, j) in product(b, a))

def main():
    wordlist = read_file('all_words.txt')
    length_sorted_wordlist = sorted(wordlist, key=lambda x: len(x))

    def compare(y):
        def func(x):
            return y - len(x)
        return func

    # find breakpoints for lengths of words
    breakpoints = {
        i: binary_search(length_sorted_wordlist, compare(i)) 
        for i in range(2, len(length_sorted_wordlist[-1]))
    }

    total_word_count = len(length_sorted_wordlist)
    for l in range(2, 23):
        start_time = perf_counter()

        print(f"looking for words with length {l}, like {length_sorted_wordlist[breakpoints[l]]}")

        range_size = breakpoints[l + 1] - breakpoints[l]
        size_to_end = total_word_count - ((breakpoints[l + 1] + breakpoints[l]) // 2)
        range_total = (range_size * size_to_end) + range_size // 2
        count = 0

        for i in range(breakpoints[l], breakpoints[l + 1]):
            print(f'progress {count} / {range_total}', end='\r')
            base = length_sorted_wordlist[i]

            matching_start = [word for word in length_sorted_wordlist[i+1:] if word[:l] == base]
            matching_end = [word for word in length_sorted_wordlist[i+1:] if word[-l:] == base]

            if len(matching_start) and len(matching_end):
                combinations = make_combinations(base, matching_start, matching_end)
                append_to_file(f'output/output{l:02d}.txt', combinations)
            count += (total_word_count - i)

        end_time = perf_counter()
        print(f"{count} words checked. time elapsed: {end_time - start_time:0.1f} seconds")

if __name__ == '__main__':
    main()
