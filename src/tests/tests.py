from ..roller import execute_command 

tests = [
    "4d8 + 1",
    "5d6+1d4|kh:3|cn:>4",
    "4d6 | kh:2 + 1",
    "d10",
    "2+3d10",
    "3df",
    "5d6+1|kl:1",    
    "4d6 | kl:2 + 5d10 |cn:>4",
    "3d6|ex:5,6 | cn:6",
    "4d6|ex:5..6",
    "3d6|rr:1,2",
]


def run_tests_all():

    for expression in tests:
        result = execute_command(expression)

        if result[0]:
            print(f"{expression} -> {result}")
        else:
            print(f"Fail with {result[2]}")    


def run_tests_single():
    expression = "5d6+1d4"
    # result = parse_expression(expression)
    result = execute_command(expression)
    print(f"{expression} -> {result}")
    # total, log = address_commands(result)
    # print(f"total: {total}, log :{log}")


def run_tests():  # "4d6 + 1 | h:2 | c:5,6" 3d6|c:2

    run_tests_all()
    # run_tests_single()
