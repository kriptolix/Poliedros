import random
import re


def roll_dice(parameter):

    match = re.match(r'(\d+)d(\d+)', parameter)

    n_dices = int(match.group(1))
    n_sides = int(match.group(2))

    roll = []

    if n_dices == 0:
        n_dices = 1
    if n_sides == 0:
        return None

    for dice in range(n_dices):
        roll.append(random.randint(1, n_sides))

    roll.sort(reverse=True)

    results = roll
    return results


def array_trim(free_dice_array, position, number):
    if not free_dice_array:
        return None

    copy_array = free_dice_array[-1][:]

    if position == 'l':
        copy_array.sort()

    trim_array = copy_array[:number]
    trim_array.sort(reverse=True)

    results = [trim_array, sum(trim_array)]
    return results


def command_handler(input_command):

    if not input_command or 'd' not in input_command:
        return None

    # Separa os elementos do comando
    parameters = re.findall(r'(\d*d\d+|[+-]|[hl]|\d+)', input_command)

    print('Parâmetros iniciais:', parameters)

    free_dice_array = []
    kept_dice_array = []
    partial_value = 0
    total_value = 0
    signal = 1
    presentation = ''

    for p in range(len(parameters)):

        if 'd' in parameters[p]:  # testa se é um dado
            values = parameters[p].split('d')  # Divide os parâmetros

            roll = roll_dice(int(values[0] or 1), int(
                values[1]))  # Rola os dados e soma

            partial_value += roll[1]  # Adiciona ao parcial
            free_dice_array.append(roll[0])  # Registra para apresentação

        if parameters[p] in ['l', 'h']:  # testa lower ou higher
            trim_array = array_trim(free_dice_array, parameters[p], int(
                parameters[p + 1]))  # Gera subarray

            partial_value = trim_array[1]
            kept_dice_array.append(trim_array[0])

        if parameters[p] in ['+', '-']:
            if 'd' in parameters[p + 1]:
                total_value += signal * partial_value
                partial_value = 0
                signal = int(parameters[p] + '1')
            else:
                partial_value += int(parameters[p] + parameters[p + 1])

    total_value += signal * partial_value

    if not kept_dice_array:
        presentation = f'Roll: {input_command}\nResults: {
            free_dice_array}\nTotal: {total_value}'
    else:
        presentation = f'Roll: {input_command}\nResults: {
            free_dice_array}, values kept: {kept_dice_array},\nTotal: {total_value}'

    # print('Array de dados:', free_dice_array)
    # print(presentation)

    return presentation


def execute_operations(parameters):

    patt_d = r'^\d*d\d+$'
    patt_h = r'^\d*h\d+d\d+$'

    for parameter in parameters:

        if (re.match(patt_d, parameter)):
            roll_dice(parameter)

        if (re.match(patt_h, parameter)):
            match = re.match(r'^(\d*h)\d+d\d+$', parameter)
            higher_lower(match)


def validate_parameters(parameters):

    patt_d = r'^\d*d\d+$'
    patt_l = r'^\d*l\d+d\d+$'
    patt_h = r'^\d*h\d+d\d+$'
    patt_e = r'^\d*e\d+d\d+$'
    patt_i = r'^[+-]+$'
    patt_n = r'^\d+$'

    if not parameters:
        print("Parâmetros vazios")
        return

    for elemento in parameters:
        if not (re.match(patt_d, elemento)
                or re.match(patt_l, elemento)
                or re.match(patt_h, elemento)
                or re.match(patt_e, elemento)
                or re.match(patt_n, elemento)
                or re.match(patt_i, elemento)):

            print(f"Erro de sintaxe: '{elemento}'")
            return

    # return "elementos validos"


def parse_command(input_command):
    # input_command = re.sub(r'[^0-9dhle\+\-]', '', input_command)
    input_command = re.sub(' ', '', input_command)
    parameters = re.split(r'(\+|\-)', input_command)
    print('Parâmetros iniciais:', parameters)

    validate_parameters(parameters)

    execute_operations(parameters)


def higher_lower(element, name):
    
    match name:
        case "h":
            patt = r'^(\d*h)\d+d\d+$'

        case "l":
            patt = r'^(\d*l)\d+d\d+$'

    match = re.match(patt, element)

    operation = match.group(1)
    dices = element[len(operation):]

    if len(operation) > 1:
        group = int(operation[:-1])

    roll = roll_dice(dices)

    results = roll[:group] # maiores
    results = roll[-group:] # menores

    

    return results


def lower_among(range):
    patt = r'^(\d*l)\d+d\d+$'


def explode(range):
    patt = r'^(\d*e)\d+d\d+$'
