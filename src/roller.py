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

    keep = int(split[0])
    dices = split[1]

    if not keep:
        keep = 1

    roll = roll_dice(dices)

    total = f"{sum(roll)}"
    log = f"{parameter} {roll} "

    if keep < len(roll):

        match action:
            case "h":
                subroll = roll[:keep]
                excluded = roll[:len(subroll)]
                excluded.insert(0, subroll)

            case "l":
                subroll = roll[-keep:]
                excluded = roll[:-len(subroll)]
                excluded.append(subroll)

        total = f"{sum(subroll)}"
        log = f"{parameter} {excluded}"

    return [total, log]


def explode_dice(parameter):
    split = parameter.split(f"e", 1)

    limit = int(split[0])
    dices = split[1]
    pos = dices.find('d')
    faces = int(dices[pos+1:])

    if not limit:
        limit = 100

    roll = roll_dice(dices)

    for dice in roll:
        if dice == faces:

            reroll = roll_dice(f"1d{faces}")
            roll.append(reroll)
            roll.sort(reverse=True)

    total = f"{sum(roll)}"
    log = f"{parameter} {roll} "


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

        if (re.match(patt_n, parameter)):
            total = parameter
            log = parameter

        if (re.match(patt_o, parameter)):
            total = parameter
            log = " " + parameter + " "

        result = result + total
        track = track + log

    results = [eval(result), track]

    return results


def validate_parameters(parameters):

    if not parameters:
        print("Parâmetros vazios")
        return

    for elemento in parameters:
        if not (re.match(patt_d, elemento)
                or re.match(patt_l, elemento)
                or re.match(patt_h, elemento)
                or re.match(patt_e, elemento)
                or re.match(patt_n, elemento)
                or re.match(patt_o, elemento)):

            print(f"Erro de sintaxe: '{elemento}'")
            return

    # return "elementos validos"


def execute_command(input_command):

    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-)', input_command)

    # print('Parâmetros iniciais:', parameters)

    response = validate_parameters(parameters)

    if response:
        return response

    results = execute_operations(parameters)

    return results
