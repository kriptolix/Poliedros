import random


def roll_dice(expression):

    n_dices, n_sides = expression

    if n_sides == "f":
        n_sides = 3
        n_range = [-1, 1]
    else:
        n_sides = int(n_sides)
        n_range = [1, n_sides]

    if (n_dices) > 100 or (n_sides) > 1000:
        return [False, "Dices or sides beyond limit"]

    roll = []

    for dice in range(n_dices):
        roll.append(random.randint(n_range[0], n_range[1]))

    roll.sort(reverse=True)

    # print("brute roll : ", roll)

    return roll


def define_group(expression, faces):

    lenght = len(expression)

    match lenght:
        case 2:
            one, two = expression
            if one == "<":
                group = list(range(1, two))
            if one == ">":
                group = list(range(two, faces))

        case 3:
            one, two, three = expression
            if three == "..":
                group = range(one, three)
        case _:
            group = expression

    return group

def avaliate_parameters(expression):

    commands = ["count", "lower"]

    if len(expression) == 3:
        if expression[0] in commands:
            "is command, send to resolution"
            return
    

def count_in(expression):  # c(2h3d6),5,6
    total = 0
    log = ''

    parameters, dices = expression
    _, faces = dices

    group = define_group(parameters, faces)

    roll = roll_dice(dices)

    for value in roll:
        if value in (group):
            total = total + 1

    total = f"{total}"
    log = f"{expression} {roll} "

    return [total, log]
