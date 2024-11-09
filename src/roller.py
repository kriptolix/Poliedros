import random
import re

# Validation Patterns

patt_d = r'^\d*d\d+$'
patt_l = r'^\d*l\d+d\d+$'
patt_h = r'^\d*h\d+d\d+$'
patt_e = r'^\d*e\d+d\d+$'
patt_o = r'^[+-]+$'
patt_n = r'^\d+$'


def roll_dice(parameter):

    n_dices, n_sides = parameter.split('d', 1)

    if not n_dices:
        n_dices = '1'

    roll = []

    for dice in range(int(n_dices)):
        roll.append(random.randint(1, int(n_sides)))

    roll.sort(reverse=True)

    # print("brute roll : ", roll)

    return roll


def keep_subset(parameter, action):

    split = parameter.split(f"{action}", 1)

    if split[0]:
        keep = int(split[0])
    else:
        keep = 1

    dices = split[1]

    roll = roll_dice(dices)
    print(roll)

    total = f"{sum(roll)}"
    log = f"{parameter} {roll} "

    if keep < len(roll):

        match action:
            case "h":
                subroll = roll[:keep]
                excluded = roll[:-len(subroll)]
                excluded.insert(0, subroll)

            case "l":
                subroll = roll[-keep:]
                excluded = roll[:-len(subroll)]
                print("excluded2: ", excluded)

        total = f"{sum(subroll)}"
        log = f"{parameter} {excluded}"
        print(subroll)

    return [total, log]


def explode_dice(parameter):

    counter = 0

    split = parameter.split("e", 1)

    if split[0]:
        limit = int(split[0])
    else:
        limit = 50

    if limit > 50:
        limit = 50

    dices = split[1]
    pos = dices.find('d')
    faces = int(dices[pos+1:])

    roll = roll_dice(dices)

    for dice in roll:
        if dice == faces and counter < limit:
            counter = counter + 1

            reroll = roll_dice(f"1d{faces}")
            roll.append(reroll[0])
            roll.sort(reverse=True)

    total = f"{sum(roll)}"
    log = f"{parameter} {roll} "

    return [total, log]


def execute_operations(command):

    result = ""
    track = ""

    for parameter in command:

        if (re.match(patt_d, parameter)):
            roll = roll_dice(parameter)

            total = f"{sum(roll)}"
            log = f"{parameter} {roll}"

        if (re.match(patt_h, parameter)):
            total, log = keep_subset(parameter, "h")

        if (re.match(patt_l, parameter)):
            total, log = keep_subset(parameter, "l")

        if (re.match(patt_e, parameter)):
            total, log = explode_dice(parameter)

        if (re.match(patt_n, parameter)):
            total = parameter
            log = parameter

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
                or re.match(patt_n, element)
                or re.match(patt_o, element)):

            result = [False, "Sintaxe Error: ", element]
            return result

    # return "elementos validos"


def execute_command(input_command):

    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-)', input_command)

    # print('Parâmetros iniciais:', parameters)

    result = validate_parameters(parameters)

    if result:
        return result

    results = execute_operations(parameters)

    return results
