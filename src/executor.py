import random
import re

from .regexpatterns import *


def setup_parameters(parameters: list, pool: list) -> list:

    print("elements: ", parameters)

    group = []

    if len(parameters) == 3:

        if parameters[1] == "<":
            for element in pool:
                if element <= int(parameters[2]):
                    group.append(element)
            return group

        if parameters[1] == ">":
            for element in pool:
                if element >= int(parameters[2]):
                    group.append(element)
            return group

        if parameters[1] == "..":
            for element in pool:
                if element >= int(parameters[0]) and element <= int(parameters[2]):
                    group.append(element)
            return group

    for parameter in parameters:
        group.append(int(parameter))

    # print("group: ", group)

    return group


def roll_dice(expression: str) -> list:

    n_dices, _, n_sides = expression

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

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    command = elements[0]
    parameters = elements[2:]

    group = setup_parameters(parameters, pool)
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

    parameter_log = ''

    for parameter in parameters:
        parameter_log = parameter_log + f" {parameter}"

    total = f"{total}"
    log = f" {text}{parameter_log} = {total} "

    return [total, log]


def keep_subset(expression: str, pool: list) -> list:

    elements = re.split(r'(:|\||\.\.|<|>)', expression)

    keep = int(elements[2])

    match elements[0]:
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
    log = f" {text} {keep} = {subroll} "

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

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    parameters = elements[4:]
    dice_faces = re.split('d', elements[0])

    # print("elements, parameters :", elements, parameters)

    command = "Explode"

    pool, log = roll_dice(elements[0])

    # print("pool, log: ", pool, log)

    group = setup_parameters(parameters, pool)

    counter = 0

    dice = ['1', 'd', dice_faces[1]]

    initial_pool = pool

    for element in initial_pool:
        if element in group:

            _recursive_roll(dice, group, False)

    pool.sort(reverse=True)

    total = pool
    log = f"{command} {group} in {log}"

    return [total, log]


def reroll(expression):  # think about the best results output

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    parameters = elements[4:]
    dice_faces = re.split('d', elements[0])

    # print("elements, parameters :", elements, parameters)

    command = "Reroll"

    pool, log = roll_dice(elements[0])

    # print("pool, log: ", pool, log)

    group = setup_parameters(parameters, pool)

    dice = ['1', 'd', dice_faces[1]]

    log = f"{command} {parameters} in {pool}"

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


def address_commands(expression):  

    total = 0
    pool = []
    plus_minus = None
    track = ''

    for elemment in expression:

        if plus_minus:
            value = total

            if pool:
                value = sum(pool)
                track = track + f"= {value} {plus_minus} "

            total, op_log = do_operation(
                plus_minus, value, sum(result))

            log = log + op_log
            pool = None
            plus_minus = None

        if elemment == '+' or elemment == '-':
            plus_minus = elemment
            track = track + elemment

        if isinstance(elemment, int):  # number

            total = elemment
            log = f" {elemment} "

            track = track + log
            # print("integer total, pool: ", total, pool)

        if isinstance(elemment, list):

            if len(elemment) == 3:  # dice roll

                pool, log = roll_dice(elemment)

                track = track + log
                # print("dice log, total, pool: ", log, total, pool)

            if len(elemment) == 2:  # function call
                command, parameters = elemment

                data = [total]

                if pool:
                    data = pool

                # print("cmd: ", command, parameters, data)

                match command:
                    case 'count' | 'cn' | 'check' | 'ch':
                        result, log = count_in(command, parameters, data)
                        pool = None
                        total = total + result

                    case "highest" | "lowest" | "kh" | "kl":
                        pool, log = keep_subset(command, parameters, data)
                        total = 0

                    case "explode":
                        pool, log = explode(command, parameters, data)

                    case "stratify":
                        pool, log = stratify(command, parameters, data)

                    case "reroll":
                        pool, log = reroll(command, parameters, data)

                    case "multiroll":
                        pool, log = multiroll(command, parameters, data)

                track = track + log

    if pool:
        # print("total: ", total, " pool: ", pool)
        total = total + (sum(pool))
        track = track + f"= {total}"

    # print("total, track: ", total, track)

    return [total, track]


def execute_operations(command):  

    result = ""
    track = ""
    pool = None
    operation = False

    for parameter in command:
        log = ''
        total = ''

        if (re.match(pt_dice, parameter)):
            roll, log = roll_dice(parameter)
            pool = roll

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
                pool = None

        if (re.match(pt_integer, parameter)):
            total = parameter
            log = parameter

            if operation:

                total = f" {operation} {parameter}"
                log = f" {operation} {parameter}"

                if pool:
                    total = f"{sum(roll)} {operation} {parameter}"
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
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
                pool = None

        if (re.match(pt_mr, parameter)):  # in: dice, out: list[list]

            if operation:
                raise ValueError('Multirools cant be added.')
            
            roll, log = multiroll(parameter)
            result = f'{pool}'
            break
            

        if (re.match(pt_rr, parameter)):  # in: dice, out: list
            # total, log = explode(parameter)

            print('rr ', parameter)

        if (re.match(pt_kh, parameter)
                or re.match(pt_kl, parameter)):
            values = [total]
            if pool:
                values = pool

            roll, log = keep_subset(parameter, values)
            pool = roll

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
                pool = None

        if (re.match(pt_cn, parameter)):  # in: list, out: integer

            values = [total]
            if pool:
                values = pool

            total, log = count_in(parameter, values)
            pool = None

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
       
        result = result + total
        track = track + log

    print(f"results: {result}, track: {track}, pool: {pool}")

    if pool:
        result = result + f"{sum(pool)}"

    results = [True, eval(result), track]

    return results


def execute_command(input_command):

    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-|\|)', input_command)

    fixed_param = []

    for index, param in enumerate(parameters):
        new = param
        if ((re.match(pt_ex_b, param))
            or (re.match(pt_rr_b, param))
                or (re.match(pt_mr_b, param))):

            if (re.match(pt_dice, parameters[index - 2])):
                new = f"{parameters[index - 2]}|{param}"
                fixed_param.pop(index - 2)

        fixed_param.append(new)

    print(fixed_param)

    result = execute_operations(fixed_param)

    print(result)

    return fixed_param
