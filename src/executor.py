import random
import re

from .regexpatterns import (
    pt_cn, pt_kh, pt_kl, pt_ex, pt_ex_b, pt_integer, pt_pipe,
    pt_mr, pt_mr_b, pt_rr, pt_rr_b, pt_dice, pt_operator, pt_functon,
    pt_kh_b, pt_kl_b

)


def setup_parameters(parameters: list, pool: list) -> list:

    # print("elements: ", parameters)

    log = ''

    for parameter in parameters:
        if parameter != '':
            log = f"{log} {parameter}"

    group = []

    if len(parameters) == 3:

        if parameters[1] == "<":
            for element in pool:
                if element <= int(parameters[2]):
                    group.append(element)
            return [group, log]

        if parameters[1] == ">":
            for element in pool:                
                if element >= int(parameters[2]):
                    group.append(element)
            return [group, log]

        if parameters[1] == "..":
            for element in pool:
                if element >= int(parameters[0]) and element <= int(parameters[2]):
                    group.append(element)
            return [group, log]

    for parameter in parameters:
        if parameter != ',':
            group.append(int(parameter))

    # print("group: ", group)

    return [group, log]


def roll_dice(expression: str) -> list:

    n_dices, n_sides = re.split('d', expression)

    if n_dices == '':
        n_dices = 1

    n_dices = int(n_dices)

    if n_sides == "f":
        n_sides = 3
        n_range = [-1, 1]
    else:
        n_sides = int(n_sides)
        n_range = [1, n_sides]

    roll = []

    for dice in range(n_dices):
        roll.append(random.randint(n_range[0], n_range[1]))

    roll.sort(reverse=True)

    log = f"{n_dices}d{n_sides} = {roll}"

    return [roll, log]


def count_in(expression: str, pool: list) -> list:
    total = 0

    elements = re.split(r'(:|\||\.\.|<|>|,)', expression)
    command = elements[0]
    parameters = elements[2:]

    group, parameter_log = setup_parameters(parameters, pool)
    # print("count_in group: ", group)

    roll = pool
    text = "Count"

    if command in ['check', 'ch']:
        roll = [sum(pool)]
        text = "Check"

    # print("roll: ", roll)

    for value in roll:
        # print("value: ", value, " group: ", group)
        if value in group:
            total = total + 1

    total = f"{total}"
    log = f" {text}{parameter_log} = {total} "

    return [total, log]


def keep_subset(expression: str) -> list:

    elements = re.split(r'(:|\||\.\.|<|>)', expression)

    pool, log = roll_dice(elements[0])

    keep = int(elements[4])

    match elements[2]:
        case "highest" | "kh":
            subroll = pool[:keep]
            excluded = pool[len(subroll):]
            excluded.insert(0, subroll)
            text = "Highest"

        case "lowest" | "kl":
            subroll = pool[-keep:]
            excluded = pool[:-len(subroll)]
            excluded.append(subroll)
            text = "Lowest"

    total = subroll
    log = f"{text} {keep} in {elements[0]} = {pool} = {subroll}"

    return [total, log]


def explode(expression: str) -> list:

    def _recursive_roll(dice, group, exploded):

        nonlocal counter
        nonlocal log

        if counter >= 50:
            return

        extended_roll, extended_log = roll_dice(dice)

        pool.append(extended_roll[0])
        log = f"{log}, extra {extended_log}"

        if extended_roll[0] in group:
            counter = counter + 1
            _recursive_roll(dice, group, True)
            return

        counter = 0
    ##

    elements = re.split(r'(:|\||\.\.|<|>|,)', expression)
    parameters = elements[4:]
    dice_faces = re.split('d', elements[0])

    # print("elements, parameters :", elements, parameters)

    command = "Explode"

    pool, log = roll_dice(elements[0])

    # print("pool, log: ", pool, log)

    group, parameter_log = setup_parameters(parameters, pool)

    counter = 0

    dice = f"1d{dice_faces[1]}"

    initial_pool = pool

    for element in initial_pool:
        if element in group:

            _recursive_roll(dice, group, False)

    pool.sort(reverse=True)

    total = pool
    log = f"{command} {parameter_log} in {log}"

    return [total, log]


def reroll(expression):  # think about the best results output

    elements = re.split(r'(:|\||\.\.|<|>|,)', expression)
    parameters = elements[4:]
    dice_faces = re.split('d', elements[0])

    # print("elements, parameters :", elements, parameters)

    command = "Reroll"

    pool, log = roll_dice(elements[0])

    # print("pool, log: ", pool, log)

    group, parameter_log = setup_parameters(parameters, pool)

    dice = ['1', 'd', dice_faces[1]]

    extended_pool = []

    for element in pool:
        if element in group:
            extended_roll, extended_log = roll_dice(dice)

            extended_pool.append(extended_roll[0])
            log = f"{log}, reroll {element} = {extended_roll}"
            continue

        extended_pool.append(element)

    total = extended_pool
    log = f"{command}{parameter_log} in {log} = {total} "

    # print("total, log reroll:", total, log)

    return [total, log]


def multiroll(expression: str) -> list:

    extended_roll = []

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    command = "Multiroll"

    group = int(elements[4])

    print("elements: ", elements)

    for _ in range(group):

        pool, log = roll_dice(elements[0])
        extended_roll.append(pool)

    total = extended_roll
    log = f"{command} {group} x {elements[0]}"

    print(total, log)

    return [total, log]


def address_commands(command: str) -> list:

    result = ""
    track = ""
    pool = None
    operation = False

    # print("command: ", command)

    for parameter in command:
        log = ''
        total = ''

        if (re.match(pt_dice, parameter)):
            roll, log = roll_dice(parameter)

            if operation:
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"

                if pool:
                    total = f"{sum(pool)} {operation} {sum(roll)}"
                    log = f" = {sum(pool)} {log}"
                    pool = None

                operation = False
            else:
                pool = roll

            # print(f"dice log {log}, pool {pool}, total {total}")

        if (re.match(pt_integer, parameter)):
            total = parameter
            log = parameter

            if operation:

                total = f" {operation} {parameter}"
                log = f" {operation} {parameter}"

                if pool:
                    total = f"{sum(pool)} {operation} {parameter}"
                    log = f"= {total}"

                operation = None
                pool = None

        if (re.match(pt_operator, parameter)):
            # total = parameter
            operation = parameter

        if (re.match(pt_ex, parameter)):

            roll, log = explode(parameter)
            pool = roll

            # print("explode roll, log", roll, log)

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} {log} = {sum(roll)}"
                operation = False
                pool = None

        if (re.match(pt_mr, parameter)):

            if operation:
                raise ValueError('Multirools cant be added.')

            roll, log = multiroll(parameter)
            result = f'{pool}'
            break

        if (re.match(pt_rr, parameter)):
            roll, log = reroll(parameter)
            pool = roll

            # print("explode roll, log", roll, log)

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
                pool = None

        if (re.match(pt_kh, parameter)
                or re.match(pt_kl, parameter)):

            roll, log = keep_subset(parameter)

            if operation:
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"

                if pool:
                    total = f"{sum(pool)} {operation} {sum(roll)}"
                    log = f" = {sum(pool)} {log}"
                    pool = None

                operation = False
                pool = None
            else:
                pool = roll

        if (re.match(pt_cn, parameter)):

            # print(f"total {total}, pool {pool}, result {result}")

            if pool:
                values = pool
            else:
                values = [eval(result)]

            total, log = count_in(parameter, values)
            # print("count log: ", log)
            pool = None
            result = ''

        result = result + total
        track = track + log

    # print(f"results: {result}, track: {track}, pool: {pool}")

    if pool:
        result = result + f"{sum(pool)}"

    results = [True, eval(result), track]

    return results


def validate_parameters(command):

    if not command:
        [False, None, "Empty Command"]

    for parameter in command:

        if not (re.match(pt_dice, parameter)
                or re.match(pt_integer, parameter)
                or re.match(pt_operator, parameter)
                or re.match(pt_ex, parameter)
                or re.match(pt_mr, parameter)
                or re.match(pt_rr, parameter)
                or re.match(pt_kh, parameter)
                or re.match(pt_kl, parameter)
                or re.match(pt_pipe, parameter)
                or re.match(pt_cn, parameter)):

            return [False, None, f"Sintaxe Error: {parameter}"]


def execute_command(input_command):

    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-|\|)', input_command)

    fixed_param = []

    for index, param in enumerate(parameters):  # 5d6 + 1d4 | kh:3 | cn:>4
        new = param
        if (re.match(pt_functon, param) and
                not re.match(pt_cn, param)):

            if (re.match(pt_dice, parameters[index - 2])):
                new = f"{parameters[index - 2]}|{param}"
                fixed_param.pop(index - 2)

        fixed_param.append(new)

    # print(f"Fixede param: {fixed_param}")

    validation = validate_parameters(fixed_param)

    if validation:
        return validation

    result = address_commands(fixed_param)

    return result
