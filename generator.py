from string import Template
from itertools import product, takewhile
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
    # initializing, reading file, sorting.
    wordlist = read_file(source)
    string_sorted_wordlist = sorted(wordlist)
    length_sorted_wordlist = sorted(wordlist, key=lambda x: len(x))
    breakpoints = find_breakpoints(length_sorted_wordlist)

    # Helper for checking if the remainder of a word with a part taken out is a word.
    # Used for trying to figure out if the word was a compound word.
    def is_word(word):
        if len(word) < 3:
            return False

        search_result = binary_search(string_sorted_wordlist, string_comparison_func(word))
        match = string_sorted_wordlist[search_result]
        return match == word

    total_word_count = len(wordlist)
    for l in range(MINIMUM_WORD_LENGTH, MAXIMUM_WORD_LENGTH):
        start_time = perf_counter()

        # calculations for counting progress
        range_start, range_end = breakpoints[l], breakpoints[l + 1]
        range_size = range_end - range_start
        size_to_end = total_word_count - ((range_end + range_start) // 2)
        range_total = (range_size * size_to_end) + range_size // 2
        count = 0

        print(f"looking for words with length {l}, {range_size} in total")

        # iterate all words of length l
        for i in range(range_start, range_end):
            print(f'progress {count} / {range_total}', end='\r')
            base = length_sorted_wordlist[i]

            base_index = string_sorted_wordlist.index(base)
            matching_start = [
                word for word 
                in takewhile(
                    lambda x: x[:l] == base, 
                    string_sorted_wordlist[base_index:]
                ) 
                if is_word(word[l:])
            ]

            matching_end = [
                word for word 
                in length_sorted_wordlist[i+1:] 
                if word[-l:] == base 
                    and is_word(word[:-l])
            ]

            if matching_start and matching_end:
                combinations = make_combinations(base, matching_start, matching_end)
                filename = output.safe_substitute(file_num=f'{l:02d}')
                append_to_file(filename, combinations)
            count += (total_word_count - i)

        end_time = perf_counter()
        print(f"{count} combinations checked. time elapsed: {end_time - start_time:0.1f} seconds")

if __name__ == '__main__':
    main(SOURCE, OUTPUT)
