import random
import operator
import re

# Validation Patterns

pt_integer = r'^[1-9][0-9]{0,2}+$'
pt_number = r'[1-9][0-9]{0,2}'
pt_operator = r'^[+\-]+$'
pt_dice = r'^[1-9][0-9]?d(f|[1-9][0-9]{0,2})+$'
pt_dice_prefix = r'[1-9][0-9]?d(?:f|[1-9][0-9]{0,2})'
pt_sufix = r'(?=\|[A-Za-z]{{2}}:|$)'

pt_ge_le = rf"[<>]{pt_number}"
pt_range = rf"{pt_number}\.\.{pt_number}"

pt_ex = rf"^(?:{pt_dice_prefix}\|)ex:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_rr = rf"^(?:{pt_dice_prefix}\|)rr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_mr = rf"^(?:{pt_dice_prefix}\|)mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

pt_ex_b = rf"^ex:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_rr_b = rf"^rr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_mr_b = rf"^mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

pt_cn = rf"^cn:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_st = rf"^st:(?:{pt_number})$"
pt_kh = rf"^kh:(?:{pt_number})$"
pt_kl = rf"^kl:(?:{pt_number})$"


def do_operation(operation, value, elemment):

    if operation == '+':
        op = operator.add
    if operation == '-':
        op = operator.sub

    total = op(value, elemment)
    log = f"= {elemment} {operation} {value} = {total} "

    return [total, log]


def avaliate_parameters(parameters, pool):

    group = []

    if parameters[0] == "<":
        for element in pool:
            if element <= parameters[1]:
                group.append(element)
        return group

    if parameters[0] == ">":
        for element in pool:
            if element >= parameters[1]:
                group.append(element)
        return group

    if parameters[1] == "..":
        for element in pool:
            if element >= parameters[0] and element <= parameters[2]:
                group.append(element)
        return group

    return parameters


def roll_dice(expression):

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


def count_in(command, parameters, pool):
    total = 0
    log = ''

    group = avaliate_parameters(parameters, pool)
    # print("count_in group: ", group)

    roll = pool
    text = "count"

    if command in ['check', 'ch']:
        roll = [sum(pool)]
        text = "check"

    # print("roll: ", roll)

    for value in roll:
        # print("value: ", value, " group: ", group)
        if value in group:
            total = total + 1

    total = total
    log = f"-> {text} {parameters} = {total} "

    return [total, log]


def keep_subset(command, parameters, pool):

    roll = pool

    keep = parameters[0]

    match command:
        case "highest" | "kh":
            subroll = roll[:keep]
            excluded = roll[len(subroll):]
            excluded.insert(0, subroll)
            text = "highest"

        case "lowest" | "kl":
            subroll = roll[-keep:]
            excluded = roll[:-len(subroll)]
            excluded.append(subroll)
            text = "lowest"

    total = subroll
    log = f"-> {text} {parameters} = {subroll} "

    return [total, log]


def setup_parameters(expression):

    elements = re.split(r'(:|\||\.\.)', expression)
    command = elements[2]
    dice_string = re.split('d', elements[0])

    pool, log = roll_dice(dice_string)

    group = []

    if elements[4] == "<":
        for element in pool:
            if element <= element[1]:
                group.append(element)
        return group

    if elements[4] == ">":
        for element in pool:
            if element >= elements[1]:
                group.append(element)
        return group

    if elements[5] == "..":
        for element in pool:
            if element >= elements[4] and element <= elements[6]:
                group.append(element)
        return group

    parameters = [command, group, log]

    return parameters


def explode(expression):

    parameters = re.split(r'(:|\||\.\.)', expression)
    command = parameters[2]
    pool = parameters[0]

    print(parameters)
    log_roll = []
    counter = 0

    # n_dices = int(pool[0])

    def _recursive_roll(dice, group, exploded):  # [6, [6], 3, 2]

        nonlocal counter

        if counter >= 50:
            return

        roll = roll_dice(dice)

        print('explode roll: ', roll, group)

        log_roll.append(roll[0])

        if roll[0] in group:
            counter = counter + 1
            _recursive_roll(dice, group, True)
            return

        counter = 0
    ##

    '''group = avaliate_parameters(parameters, pool)

    dice = ['1', 'd', pool[2]]

    print('explode dice, ndices: ', dice, n_dices)

    for _ in range(n_dices):

        _recursive_roll(dice, group, False)

    log_roll.sort(reverse=True)

    total = log_roll
    log = f"{command} {parameters} in {pool}"

    return [total, log]'''


def reroll(command, parameters, pool):  # think about the best results output

    log_roll = []

    group = avaliate_parameters(parameters, pool)
    roll = avaliate_pool(pool)

    log_roll.append(roll)

    dice = ['1', 'd', pool[2]]

    for number in roll:
        log_roll.append(number)

        if number in group:
            single = roll_dice(dice)
            log_roll.append(single)

    total = log_roll
    log = f"{command} {parameters} in {pool}"

    return [total, log]


def multiroll(command, parameters, pool):

    log_roll = []

    group = avaliate_parameters(parameters, pool)

    print("grupo: ", group)

    for _ in range(group[0]):

        roll = avaliate_pool(pool)
        log_roll.append(roll)

    total = log_roll
    log = f"{command} {parameters} in {pool}"

    return [total, log]


def stratify(command, parameters, pool):  # s 6,9 in 2d6
    log_roll = []

    group = avaliate_parameters(parameters, pool)
    roll = avaliate_pool(pool)

    total = log_roll
    log = f"{command} {parameters} in {pool}"

    return [total, log]


def address_commands(expression):  # 3d6 + 1d4, 1d4 + 3d6 | c:2 | h:2

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


def execute_operations(command):  # 6 - 5d6 + 1d4 |kh:3 |cn:>4

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

        if (re.match(pt_ex, parameter)):  # in: dice, out: list
            roll, log = explode(parameter)
            pool = roll

            if operation:
                total = f" {operation} {sum(roll)}"
                log = f" {operation} ({log} = {sum(roll)})"
                operation = False
                pool = None

        if (re.match(pt_mr, parameter)):  # in: dice, out: list[list]
            # total, log = explode(parameter)

            print('mr ', parameter)

        if (re.match(pt_rr, parameter)):  # in: dice, out: list
            # total, log = explode(parameter)

            print('rr ', parameter)

        if (re.match(pt_kh, parameter)  # in: list, out: list
                or re.match(pt_kl, parameter)):

            '''data = total  # eval(total)?

            if pool:
                data = pool

            total, log = keep_subset(parameter, data)'''

            print('kp ', parameter)

        if (re.match(pt_cn, parameter)):  # in: list, out: integer
            # total, log = count_in(parameter)
            print('cn', parameter)

        # stratify, entrada deve ser lista

        result = result + total
        track = track + log

    print(f"results: {result}, track: {track}")

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
