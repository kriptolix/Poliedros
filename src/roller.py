import random
import re

from .regexpatterns import (
    pt_cn, pt_kh, pt_kl, pt_ex, pt_integer, pt_pipe,
    pt_mr, pt_rr, pt_dice, pt_operator, pt_function,
    pt_kh_b, pt_kl_b, pt_ex_b, pt_rr_b, pt_dice_func

)


def setup_parameters(parameters: list, pool: list) -> list:

    # print("setup parameters: ", parameters)

    log = ''

    for parameter in parameters:
        if parameter != '':
            log = f"{log}{parameter}"

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
    log = f"{text} {parameter_log} = {total}"

    return [total, log]


def keep_subset(command: str, keep: int, pool: list, dice: str | None) -> list:

    dice_log = f"{pool}"

    if dice:
        dice_log = f"{dice} = {pool}"

    match command:
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
    log = f"{text} {keep} in {dice_log} = {subroll}"

    return [total, log]


def explode(pool: list, faces: str, parameters: list, log: str) -> list:

    def _recursive_roll(dice, group):

        nonlocal counter
        nonlocal log

        if counter >= 50:
            return

        extended_roll, extended_log = roll_dice(dice)

        pool.append(extended_roll[0])
        log = f"{log}, extra {extended_log}"

        if extended_roll[0] in group:
            counter = counter + 1
            _recursive_roll(dice, group)
            return

        counter = 0
    ##

    command = "Explode"

    group, parameter_log = setup_parameters(parameters, pool)

    counter = 0

    dice = f"1d{faces}"

    initial_pool = pool

    for element in initial_pool:
        if element in group:

            _recursive_roll(dice, group)

    pool.sort(reverse=True)

    total = pool
    log = f"{command} {parameter_log} in {log} = {pool}"

    return [total, log]


def reroll(pool: list, parameters: list, faces: str, log: str) -> list:

    command = "Reroll"

    group, parameter_log = setup_parameters(parameters, pool)

    dice = f"1d{faces}"

    extended_pool = []

    for element in pool:
        if element in group:
            extended_roll, extended_log = roll_dice(dice)

            extended_pool.append(extended_roll[0])
            log = f"{log}, reroll {element} = {extended_roll}"
            continue

        extended_pool.append(element)

    total = extended_pool
    log = f"{command} {parameter_log} in {log} = {total}"

    # print("total, log reroll:", total, log)

    return [total, log]


def multiroll(expression: str) -> list:

    extended_roll = []

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    command = "Multiroll"

    group = int(elements[4])

    # print("elements: ", elements)

    for _ in range(group):

        pool, log = roll_dice(elements[0])
        extended_roll.append(pool)

    total = extended_roll
    log = f"{command} {group} x {elements[0]}"

    # print(total, log)

    return [total, log]


def next_is_function(commands: list, actual: int) -> bool:

    if ((actual + 2 < len(commands)) and
            re.match(pt_function, commands[actual + 2])):
        return True

    return False


def address_commands(commands: list, testing: bool = None) -> list:

    result = ""
    track = ""
    pool = None
    operation = False
    working_dice = None

    if testing:
        pool = commands[0]

    for index, parameter in enumerate(commands):
        log = ''
        total = ''

        # print("parameter: ", parameter)

        if (re.match(pt_dice, parameter)):
            roll, log = roll_dice(parameter)
            working_dice = parameter

            if operation:
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"

                if pool:
                    total = f"{sum(pool)} {operation} {sum(roll)}"
                    log = f"= {sum(pool)}{log}"
                    pool = None

                operation = False
            else:
                pool = roll

            # print(f"dice log {log}, pool {pool}, total {total}")

        if (re.match(pt_integer, parameter)):
            total = parameter
            log = parameter

            if operation:
                total = f"{operation} {parameter}"
                log = f"{operation} {parameter}"

                if pool:
                    total = f"{sum(pool)} {operation} {parameter}"
                    log = f"= {total}"

                operation = None
                pool = None

        if (re.match(pt_operator, parameter)):
            operation = parameter

            if pool:
                total = f"{sum(pool)}"
                log = f"= {sum(roll)}"
                pool = None

        if (re.match(pt_ex, parameter)):

            elements = re.split(r'(:|\||\.\.|<|>|,)', parameter)
            parameters = elements[4:]
            _, faces = re.split('d', elements[0])

            dice_pool, dice_log = roll_dice(elements[0])
            working_dice = elements[0]

            roll, log = explode(dice_pool, faces, parameters, dice_log)
            pool = roll

            if operation:
                if not next_is_function(commands, index):
                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)}"
                    operation = False
                    pool = None

        if (re.match(pt_ex_b, parameter)):  # ex:>5

            elements = re.split(r'(:|\||\.\.|<|>)', parameter)
            parameters = elements[2:]

            # print("splited elements: ", elements)

            _, faces = re.split('d', working_dice)

            roll, log = explode(pool, faces, parameters, f"{pool}")
            pool = roll

            if operation:
                if not next_is_function(commands, index):
                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)}"
                    operation = False
                    pool = None

        if (re.match(pt_mr, parameter)):

            if operation:
                raise ValueError('Multirools cant be added.')

            roll, log = multiroll(parameter)
            result = f'{pool}'
            break

        if (re.match(pt_rr, parameter)):

            elements = re.split(r'(:|\||\.\.|<|>|,)', parameter)
            parameters = elements[4:]
            _, faces = re.split('d', elements[0])

            dice_pool, dice_log = roll_dice(elements[0])
            working_dice = elements[0]

            roll, log = reroll(dice_pool, parameters, faces, dice_log)
            pool = roll

            # print("explode roll, log", roll, log)

            if operation:
                if not next_is_function(commands, index):
                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)}"
                    operation = False
                    pool = None

        if (re.match(pt_rr_b, parameter)):

            elements = re.split(r'(:|\||\.\.|<|>)', parameter)
            _, faces = re.split('d', working_dice)
            parameters = elements[2:]

            roll, log = reroll(pool, parameters, faces, f"{pool}")

            if operation:
                if not next_is_function(commands, index):
                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)})"
                    operation = False
                    pool = None

        if (re.match(pt_kh, parameter)
                or re.match(pt_kl, parameter)):

            elements = re.split(r'(:|\||\.\.|<|>)', parameter)

            dice_pool, _ = roll_dice(elements[0])
            working_dice = elements[0]

            roll, log = keep_subset(elements[2],
                                    int(elements[4]),
                                    dice_pool,
                                    elements[0])

            if operation:

                if not next_is_function(commands, index):

                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)}"

                    if pool:
                        total = f"{sum(pool)} {operation} {sum(roll)}"
                        log = f"= {sum(pool)} {log}"
                        pool = None

                    operation = False
                    pool = None
            else:
                pool = roll

        if (re.match(pt_kh_b, parameter)
                or re.match(pt_kl_b, parameter)):

            elements = re.split(r'(:|\||\.\.|<|>)', parameter)

            if pool:

                roll, log = keep_subset(elements[0],
                                        int(elements[2]),
                                        pool,
                                        None)

                if operation:

                    if not next_is_function(commands, index):

                        total = f"{operation} {sum(roll)}"
                        log = f"{operation} {log} = {sum(roll)}"

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
        track = track + " " + log

    # print(f"results: {result}, track: {track}, pool: {pool}")

    if pool:
        result = f"{result} {sum(pool)}"

    results = [True, eval(result), track]

    return results


def validate_elements(commands: list) -> list | None:

    if not commands:
        [False, None, "Empty Command"]

    for index, element in enumerate(commands):

        if not (re.match(pt_dice, element)
                or re.match(pt_integer, element)
                or re.match(pt_operator, element)
                or re.match(pt_ex, element)
                or re.match(pt_rr, element)
                or re.match(pt_kh, element)
                or re.match(pt_kl, element)
                or re.match(pt_ex_b, element)
                or re.match(pt_rr_b, element)
                or re.match(pt_kh_b, element)
                or re.match(pt_kl_b, element)
                or re.match(pt_cn, element)):

            return [False, None, f"Sintaxe Error: {element}"]

        if (re.match(pt_ex_b, element)
                or re.match(pt_rr_b, element)
                or re.match(pt_kh_b, element)
                or re.match(pt_kl_b, element)):

            if (re.match(pt_integer, commands[index - 1])
                    or re.match(pt_operator, commands[index - 1])):

                return [False, None, f"Sintaxe Error: {element} not preceded"]


def execute_command(commands: str) -> list:

    commands = re.sub(' ', '', commands)
    parameters = re.split(r'(\+|\-|\|)', commands)

    fixed_param = []

    for index, param in enumerate(parameters):  # 5d6 + 1d4 | kh:3 | cn:>4,
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

        fixed_param.append(new)
    # print(f"Fixede param: {fixed_param}")

    validation = validate_elements(fixed_param)

    if validation:
        return validation

    result = address_commands(fixed_param)

    return result
