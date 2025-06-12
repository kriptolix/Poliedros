import re


from ..roller import execute_command, validate_elements
from .teststrings import tests

from ..regexpatterns import (
    pt_dice, pt_function, pt_cn, pt_pipe
)


def test_validate_elements(commands):
    commands = re.sub(' ', '', commands)
    parameters = re.split(r'(\+|\-|\|)', commands)    

    fixed_param = []

    for index, param in enumerate(parameters):  # # 1d4 | kh:3 + 5d6 | cn:>4,
        new = param

        if (re.match(pt_pipe, param)):
            continue

        if (index < (len(parameters) - 1) and
            re.match(pt_dice, param) and
                re.match(pt_function, parameters[index + 2]) and
                not re.match(pt_cn, parameters[index + 2])):

            new = f"{param}|{parameters[index + 2]}"

        if (index >= 2 and
            re.match(pt_function, param) and
                re.match(pt_dice, parameters[index - 2]) and
                not re.match(pt_cn, param)):
            continue

        # print(f"new: {new}, list: {fixed_param}")
        fixed_param.append(new)

    print(f"Fixede param: {fixed_param}")

    validation = validate_elements(fixed_param)

    if validation:
        print(f"\x1b[0;31;40m Fail \x1b[0m: "
              f"Sintaxe test of {commands} fail with {validation[2]}")
        return

    # print(f"\x1b[0;32;40m Ok \x1b[0m: Sintaxe test of {commands} pass")

    print(f"{commands} -> {fixed_param}")


def run_tests_all():

    all_pass = True

    for expression in tests:
        test_validate_elements(expression)

        result, total, track = execute_command(expression)

        if not result:
            all_pass = False
            print(f"\x1b[0;31;40m Fail \x1b[0m: Fail with {result[2]}")

    if all_pass:
        print("\x1b[0;32;40m Ok \x1b[0m> All testes pass")


def run_tests_single():
    expression = "3d6|kh:2|ex:>5"
    # result = parse_expression(expression)
    result = execute_command(expression)
    print(f"{expression} -> {result}")
    # total, log = address_commands(result)
    # print(f"total: {total}, log :{log}")


def run_tests():  # "4d6 + 1 | h:2 | c:5,6" 3d6|c:2

    run_tests_all()
    # run_tests_single()
    # test_validate_elements("4d6|kl:2+5d10|cn:>4")
