import random
import re

# Validation Patterns

patt_d = r'^\d*d\d+$'
patt_l = r'^\d*l\d+d\d+$'
patt_h = r'^\d*h\d+d\d+$'
patt_e = r'^\d*e\d+d\d+$'
# patt_o = r'^[+\-()]+$'
patt_o = r'^[+-]+$'
patt_n = r'^\d+$'
patt_c = r'^c\d+d\d+(?:,\d+)+$'
# patt_s = r'^s\d+d\d+\|(?:\d+(?:,\d+)*)\|(?:\d+(?:,\d+)*)\|(?:\d+(?:,\d+)*)$'
patt_p = r'^\(.+?\)+$'


def roll_dice(parameter):

    n_dices, n_sides = parameter.split('d', 1)

    if not n_dices:
        n_dices = '1'

    if (int(n_dices)) > 100 or (int(n_sides)) > 1000:
        return [False, "Dices or sides beyond limit"]

    roll = []

    for dice in range(int(n_dices)):
        roll.append(random.randint(1, int(n_sides)))

    roll.sort(reverse=True)

    # print("brute roll : ", roll)

    return roll


def stratify(parameter):  # s2d6,6,9    

    "this not work without, or is pretty useless, without compose rolls"


def count_in(parameter):  # c3d6,5,6
    total = 0
    log = ''

    split = parameter.split(",")

    # print("split: ", split)

    _, dice = split[0].split("c")

    split.pop(0)

    numbers = []

    for s in split:
        numbers.append(int(s))

    roll = roll_dice(dice)

    for value in roll:
        if value in (numbers):
            total = total + 1

    total = f"{total}"
    log = f"{parameter} {roll} "

    return [total, log]


def keep_subset(parameter, action):

    split = parameter.split(f"{action}", 1)

    if split[0]:
        keep = int(split[0])
    else:
        keep = 1

    dices = split[1]

    roll = roll_dice(dices)

    if not roll[0]:
        print("invalid")
        return roll

    # print(roll)

    total = f"{sum(roll)}"
    log = f"{parameter} {roll} "

    if keep < len(roll):

        match action:
            case "h":
                subroll = roll[:keep]
                excluded = roll[len(subroll):]
                excluded.insert(0, subroll)

            case "l":
                subroll = roll[-keep:]
                excluded = roll[:-len(subroll)]
                excluded.append(subroll)

        total = f"{sum(subroll)}"
        log = f"{parameter} {excluded}"
        print(subroll)

    return [total, log]


def explode_dice(parameter):

    sum_roll = []
    log_roll = []
    counter = 0

    def _recursive_roll(dice, exploded):  # [6, [6], 3, 2]

        nonlocal counter

        if counter >= limit:
            return

        roll = roll_dice(dice)

        log_roll.append(roll[0])
        sum_roll.append(roll[0])

        if roll[0] == int(n_sides):
            counter = counter + 1
            _recursive_roll(dice, True)
            return

        counter = 0
    ##

    split = parameter.split("e", 1)

    if split[0]:
        limit = int(split[0])
    else:
        limit = 50

    if limit > 50:
        limit = 50

    dices = split[1]

    n_dices, n_sides = dices.split('d', 1)

    for _ in range(int(n_dices)):

        _recursive_roll(f"1d{n_sides}", False)

    log_roll.sort(reverse=True)

    total = f"{sum(sum_roll)}"
    log = f"{parameter} {log_roll}"

    return [total, log]


def execute_operations(command):

    result = ""
    track = ""

    for parameter in command:

        if (re.match(patt_d, parameter)):
            roll = roll_dice(parameter)

            if not roll[0]:
                return [False, None, roll[1]]

            total = f"{sum(roll)}"
            log = f"{parameter} {roll}"

        if (re.match(patt_h, parameter)):
            total, log = keep_subset(parameter, "h")

        if (re.match(patt_l, parameter)):
            total, log = keep_subset(parameter, "l")

        if (re.match(patt_e, parameter)):
            total, log = explode_dice(parameter)

        if (re.match(patt_c, parameter)):
            total, log = count_in(parameter)

        if (re.match(patt_n, parameter)):
            total = parameter
            log = parameter

            if not total:
                return [False, None, log]

        if (re.match(patt_o, parameter)):
            total = parameter
            log = " " + parameter + " "

        result = result + total
        track = track + log

    results = [True, eval(result), track]

    return results


def validate_parameters(parameters):

    if not parameters:
        print("Parâmetros vazios")
        return

    for element in parameters:
        if not (re.match(patt_d, element)
                or re.match(patt_l, element)
                or re.match(patt_h, element)
                or re.match(patt_e, element)
                or re.match(patt_c, element)
                or re.match(patt_n, element)
                or re.match(patt_o, element)):

            return [False, None, f"Sintaxe Error: {element}"]

    # return "elementos validos"


def execute_command(input_command):

    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-)', input_command)

    # print('Parâmetros iniciais:', parameters)

    validation = validate_parameters(parameters)

    if validation:
        return validation

    results = execute_operations(parameters)

    return results
