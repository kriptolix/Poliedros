import random


def roll_dice():

    roll = []

    for _ in range(2):
        roll.append(random.randint(1, 12))

    return roll


def evaluate_agr(roll, stadard, superior):

    if roll >= stadard:

        if roll >= superior:

            return 3

        return 2

    return 1


def evaluate_atn(roll, stadard, superior):

    if roll >= stadard:

        if roll >= superior:

            return 1

        return 2

    return 3


def evaluate_ctr(roll, cost, full):

    if roll >= cost:

        if roll >= full:

            return 3

        return 2

    return 1


def test(ctr, agr, atn):

    roll = roll_dice()

    c_value = roll[0] + ctr

    controll = evaluate_ctr(c_value, 7, 11)

    if controll > 1:

        p_value = roll[0] + agr

        potence = evaluate_agr(p_value, 12, 14)

        return [controll, potence]

    p_value = roll[0] + atn

    potence = evaluate_atn(p_value, 4, 6)

    return [controll, potence]


success = 0
cost = 0
fail = 0

causado = [0, 0, 0]
sofrido = [0, 0, 0]

for _ in range(0, 100):

    result = test(2, 2, 2)

    if result[0] == 3:

        success = success + 1

        if result[0] == 3:
            causado[2] = causado[2] + 1
        if result[0] == 2:
            causado[1] = causado[1] + 1
        if result[0] == 1:
            causado[0] = causado[0] + 1

    if result[0] == 2:

        cost = cost + 1

        sofrido[0] = sofrido[0] + 1

        if result[1] == 3:
            causado[2] = causado[2] + 1
        if result[1] == 2:
            causado[1] = causado[1] + 1
        if result[1] == 1:
            causado[0] = causado[0] + 1

    if result[0] == 1:

        fail = fail + 1

        if result[1] == 3:
            sofrido[2] = sofrido[2] + 1
        if result[1] == 2:
            sofrido[1] = sofrido[1] + 1
        if result[1] == 1:
            sofrido[0] = sofrido[0] + 1

print(f"success: {success}, cost: {cost} fail: {fail} ")
print(f"causado: parcial: {causado[0]},"
      f" moderado: {causado[1]},"
      f" intenso: {causado[2]}")

print(f"sofrido: parcial: {sofrido[0]},"
      f" moderado: {sofrido[1]},"
      f" intenso: {sofrido[2]}")
