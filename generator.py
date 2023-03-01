from string import Template
from itertools import product
from time import perf_counter

MINIMUM_WORD_LENGTH = 3
MAXIMUM_WORD_LENGTH = 16
SOURCE = 'all_words.txt'
OUTPUT = Template('output/output$file_num.txt')

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return [i.strip() for i in f.readlines()]
    
def append_to_file(path, data):
    with open(path, 'a', encoding='utf-8') as f:
        for line in data:
            f.write(f"{line}\n")

def binary_search(arr, compare):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if compare(arr[m]) > 0:
            lo = m + 1
        elif compare(arr[m]) < 0:
            hi = m - 1
        else:
            return m
    return -1

def length_comparison_func(y):
    def func(x):
        return y - len(x)
    return func
    
def string_comparison_func(word):
    def func(x):
        if x == word:
            return 0
        if x < word:
            return 1
        return -1
    return func

def find_breakpoints(sorted_wordlist):
    return {
        i: binary_search(sorted_wordlist, length_comparison_func(i)) 
        for i in range(2, len(sorted_wordlist[-1]))
    }

def make_combinations(base, a, b):
    l = len(base)
    return (f"{i}{j[l:]}" for (i, j) in product(b, a))

def main(source, output):
    wordlist = read_file(source)
    length_sorted_wordlist = sorted(wordlist, key=lambda x: len(x))
    breakpoints = find_breakpoints(length_sorted_wordlist)

    total_word_count = len(wordlist)
    for l in range(MINIMUM_WORD_LENGTH, MAXIMUM_WORD_LENGTH):
        start_time = perf_counter()

        print(f"looking for words with length {l}, like {length_sorted_wordlist[breakpoints[l]]}")

        range_size = breakpoints[l + 1] - breakpoints[l]
        size_to_end = total_word_count - ((breakpoints[l + 1] + breakpoints[l]) // 2)
        range_total = (range_size * size_to_end) + range_size // 2
        count = 0

        for i in range(breakpoints[l], breakpoints[l + 1]):
            print(f'progress {count} / {range_total}', end='\r')
            base = length_sorted_wordlist[i]

            def isWord(word):
                if len(word) < 3:
                    return False

                search_result = binary_search(wordlist, string_comparison_func(word))
                match = wordlist[search_result]
                return match == word

            matching_start = [word for word in length_sorted_wordlist[i+1:] if word[:l] == base and isWord(word[l:])]

            matching_end = [word for word in length_sorted_wordlist[i+1:] if word[-l:] == base and isWord(word[:-l])]

            if len(matching_start) and len(matching_end):
                combinations = make_combinations(base, matching_start, matching_end)
                filename = output.safe_substitute(file_num=f'{l:02d}')
                append_to_file(filename, combinations)
            count += (total_word_count - i)

        end_time = perf_counter()
        print(f"{count} words checked. time elapsed: {end_time - start_time:0.1f} seconds")

if __name__ == '__main__':
    main(SOURCE, OUTPUT)
