from .commandparser import command_parser, run_postorder
from .executor import address_commands

tests = ["count 5,6 in (highest 2 in 5d6)"]

tests2 = [
    "explode1in4d6",
    "explode 1 in 4d6",
    "explode 5,6 in 4d6",
    "explode 3..5 in 4d10",
    "explode in 4d6",
    "5d6",
    "d10",
    "highest 2 in 4d10",
    "highest in 3d8",
    "lowest 3 in 6d12",
    "lowest in 4d10",
    "count 6 in 5d6",
    "count 3,4 in 6d8",
    "count 2..4 in 8d10",
    "reroll < 3 in 4d12",
    "reroll > 4 in 5d10",
    "reroll 3..5 in 4d12",
    "3d6+3",
    "(explode in 4d10)-1",
    "highest 2 in 6d10 + 5",
    "3d6+2-1",
    "(3d6)+5",
    "count 5,6 in (highest 2 in 5d6)",
    "3d6+(count 6 in 3d6)"
]


def test_parser():
    for test in tests:
        result = command_parser(test)
        print(f"{test} -> {result}")
        print(run_postorder(result))


def run_tests():
    expression = "count 5,6 in (highest 2 in 5d6)"
    result = command_parser(expression)
    print(f"{expression} -> {result}")
    total, log = address_commands(result)
    print(f"total: {total}, log :{log}")
