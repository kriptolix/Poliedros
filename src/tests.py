from .commandparser import parse_expression
from .executor import split_elements

tests = [
    ("5d6+1d4|h:3..5|c:>4",
     [[5, 'd', 6], '+', [1, 'd', 4], ['h', [3, '..', 5]], ['c', ['>', 4]]]),
    ("4d6 | h:2 + 1",
     [[4, 'd', 6], ['h', [2]], '+', 1]),
    ("d10",
     [[1, 'd', 10]]),
    ("3df",
     [[3, 'd', 'f']])
]


def run_tests():  # "4d6 + 1 | h:2 | c:5,6" 3d6|c:2
    expression = "5d6+1d4|h:3..5|c:>4"
    result = parse_expression(expression)
    print(f"{expression} -> {result}")
    # total
    # total, log = split_elements(result)
    # print(f"total: {total}, log :{log}")
