from .commandparser import parse_expression
from .executor import address_commands

tests = [
    "5d6+1d4|kh:3|cn:>4",
    "4d6 | kh:2 + 1",
    "d10",
    "2+3d10",
    "3df",
    "5d6+1|kh:5",
    "4d6 | kh:2 + 5d10 |cn:>4"
]


def run_tests_all():

    for expression in tests:
        result = parse_expression(expression)
        print(f"{expression} -> {result}")
        total, log = address_commands(result)
        print(f"total: {total}, log :{log}")


def run_tests_single():
    expression = "5d6+1d4"
    result = parse_expression(expression)
    print(f"{expression} -> {result}")
    total, log = address_commands(result)
    print(f"total: {total}, log :{log}")


def run_tests():  # "4d6 + 1 | h:2 | c:5,6" 3d6|c:2

    run_tests_all()
    # run_tests_single()
