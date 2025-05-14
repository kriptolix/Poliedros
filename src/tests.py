from .commandparser import command_parser
from .executor import split_elements

tests = ["count 5,6 in (highest 2 in 5d6)"]

tests2 = [
    "explode 1 in 4d6", "4d6|h:2|c:5,6"
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

def run_tests():  # 5d6:h2:c5,6
    expression = "count 5,6 in (highest 2 in 5d6)"
    result = command_parser(expression)
    print(f"{expression} -> {result}")
    # total  
    total, log = split_elements(result)
    print(f"total: {total}, log :{log}")
