import random


funcions_list = ["count", "highest"]


def avaliate_pool(pool):

    # print("avaliate pool, pool: ", pool)

    if len(pool) == 3:
        if pool[0] in funcions_list:  # checa se é função

            total, log = address_commands(pool)

            # print("avaliate pool, address_commands total: ", total)

            return total

        total = roll_dice(pool)
        # print("avaliate pool, roll_dice total: ", total)
        return total

    return pool


def avaliate_parameters(parameters, pool):

    lenght = len(parameters)

    match lenght:
        case 2:  # greater/smaller
            one, two = parameters
            if one == "<":
                group = range(1, int(two))
            if one == ">":
                _, faces = pool
                group = range(int(two), int(faces))

        case 3:  # range or function
            one, two, three = parameters
            if one in funcions_list:
                total, log = address_commands(parameters)

                # print("avaliate parameters, command return: ", total)

                return total

            if three == "..":
                group = range(int(one), int(three))

    group = [int(item) for item in parameters]

    # print("avaliate parameters, group return: ", group)

    return group


def roll_dice(expression):

    n_dices, _, n_sides = expression

    # print("roll dice expression: ", expression)

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

    # print("roll dice roll: ", roll)

    return roll


def count_in(command, parameters, pool):
    total = 0
    log = ''

    group = avaliate_parameters(parameters, pool)
    # print("count_in group: ", group)

    roll = avaliate_pool(pool)
    # print("count_in roll: ", roll)

    for value in roll:
        # print("value: ", value, " group: ", group)
        if value in group:
            total = total + 1

    total = total
    log = f"{command} {parameters} in {pool}"

    return [total, log]


def keep_subset(command, parameters, pool):

    group = avaliate_parameters(parameters, pool)
    # print("keep_subset group: ", group)

    roll = avaliate_pool(pool)
    # vprint("keep_subset roll: ", roll)

    keep = group[0]

    match command:
        case "highest" | "h":
            subroll = roll[:keep]
            excluded = roll[len(subroll):]
            excluded.insert(0, subroll)

        case "l":
            subroll = roll[-keep:]
            excluded = roll[:-len(subroll)]
            excluded.append(subroll)

    total = sum(subroll)
    log = f"{command} {parameters} in {pool} {subroll}"
    # print(subroll)

    return [total, log]


def explode(command, parameters, pool):

    log_roll = []
    counter = 0

    n_dices = int(pool[0])

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

    group = avaliate_parameters(parameters, pool)

    dice = ['1', 'd', pool[2]]

    print('explode dice, ndices: ', dice, n_dices)

    for _ in range(n_dices):

        _recursive_roll(dice, group, False)

    log_roll.sort(reverse=True)

    total = log_roll
    log = f"{command} {parameters} in {pool}"

    return [total, log]


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


def address_commands(expression):

    command, parameters, pool = expression

    match command:
        case "count":
            total, log = count_in(command, parameters, pool)

        case "highest" | "lowest":
            total, log = keep_subset(command, parameters, pool)

        case "explode":
            total, log = explode(command, parameters, pool)

        case "stratify":
            total, log = stratify(command, parameters, pool)

        case "reroll":
            total, log = reroll(command, parameters, pool)

        case "multiroll":
            total, log = multiroll(command, parameters, pool)

    return [total, log]


def split_elements(expression):

    total = 0
    track = ""

    for parameter in expression:        

        if isinstance(parameter, str):
            print("parametro")
            partial = 0
            log = " " + parameter + " "

        elif isinstance(parameter, int):
            print("inteiro")
            partial = parameter
            log = str(parameter)

        else:
            print("função")
            partial, log = address_commands(parameter)

        total = total + partial
        track = track + log

    return [total, track]
