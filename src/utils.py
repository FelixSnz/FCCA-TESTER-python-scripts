from string import ascii_lowercase
import itertools

def range_alpha(start:str, lenght:int):
    alphas = []
    start_passed = False

    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            s = "".join(s)
            if s == start.lower():
                start_passed = True
            if start_passed:
                alphas.append(s.upper())
            if len(alphas) == lenght:
                return alphas



print(range_alpha("AZ", 50))