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

    return roll


def define_group(parameters, pool):
    
    lenght = len(parameters)

    match lenght:
        case 2:
            one, two = list(map(int, parameters))
            if one == "<":
                group = list(range(1, two))
            if one == ">":
                _, faces = pool  
                group = list(range(two, faces))

        case 3:
            one, two, three = list(map(int, parameters))
            if three == "..":
                group = range(one, three)

    group = list(map(int, parameters))

    return group


def avaliate_parameters(parameters, pool):

    if len(parameters) == 3:
        if isinstance(parameters[0], str):

            _, total = address_commands(parameters)

            return total

    return define_group(parameters, pool)


def avaliate_pool(pool):

    if len(pool) == 3:
        if isinstance(pool[0], str):
            print("avaliate pool, pool: ", pool)

            _, total = address_commands(pool)

            print("avaliate pool, total: ", total)

            return total

    total = roll_dice(list(map(int, pool)))

    return total


def count_in(command, parameters, pool):
    total = 0
    log = ''

    group = avaliate_parameters(parameters, pool)
    print("group: ", group)

    roll = avaliate_pool(pool)
    print("roll: ", roll)

    for value in roll:
        if value in (group):
            total = total + 1

    total = f"{total}"
    log = f"{command} {parameters} in {pool}"

    return [total, log]


def keep_subset(command, parameters, pool):

    group = avaliate_parameters(parameters, pool)
    print("group: ", group)
    
    roll = avaliate_pool(pool)
    print("roll: ", roll)
    
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

    total = f"{sum(subroll)}"
    log = f"{command} {parameters} in {pool}"
    print(subroll)

    return [total, log]


def address_commands(expression):

    command, parameters, pool = expression
    print("command: ", command)
    match command:
        case "count":            
            total, log = count_in(command, parameters, pool)
            
        case "highest":            
            total, log = keep_subset(command, parameters, pool)
            
    return [total, log]
