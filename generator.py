from itertools import product

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

def compare_word(base, word):
    l = len(base)
    if word[:l] == base:
        return 1
    elif word[-l:] == base:
        return 2
    return 0

def make_combinations(base, a, b):
    l = len(base)
    # for (i, j) in product(b, a):
    #     print(f"{i}{j[l:]}", i, j)
    return [f"{i}{j[l:]}" for (i, j) in product(b, a)]

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
    for l in range(8, 20):
        print(f"looking for words with length {l}, like {length_sorted_wordlist[breakpoints[l]]}")
        range_size = breakpoints[l + 1] - breakpoints[l]
        size_to_end = total_word_count - ((breakpoints[l + 1] + breakpoints[l]) // 2)
        range_total = range_size * size_to_end
        count = 0
        for i in range(breakpoints[l], breakpoints[l + 1]):
            print(f'progress {count} / {range_total}', end='\r')
            base = length_sorted_wordlist[i]
            a, b = [], []
            for word in length_sorted_wordlist[i:]:
                if base == word:
                    continue
                result = compare_word(base, word)
                if result == 1:
                    a.append(word)
                elif result == 2:
                    b.append(word)
            if len(a) and len(b):
                combinations = make_combinations(base, a, b)
                append_to_file(f'output{l}.txt', combinations)
            count += (total_word_count - i)

if __name__ == '__main__':
    main()
