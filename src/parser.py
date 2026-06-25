import re
from pprint import pprint

pt_dice = r'^(?:[1-9][0-9]?)?d(?:f|[1-9][0-9]{0,2})+$'


def parse_function(token: str) -> dict:

    name, raw_value = token.split(":", 1)

    raw_value = raw_value.strip()
    
    if ".." in raw_value:

        start, end = raw_value.split("..")

        return {
            "name": name,
            "selector": {
                "type": "range",
                "from": int(start),
                "to": int(end)
            }
        }
    
    match = re.match(r"(>=|<=|!=|>|<|=)(.+)", raw_value)

    if match:

        op = match.group(1)
        value = match.group(2)

        try:
            value = int(value)
        except ValueError:
            pass

        return {
            "name": name,
            "selector": {
                "type": "compare",
                "op": op,
                "value": value
            }
        }
   
    try:
        value = int(raw_value)

        return {
            "name": name,
            "selector": {
                "type": "number",
                "value": value
            }
        }

    except ValueError:

        # fallback (caso futuro: flags, check, etc)
        return {
            "name": name,
            "selector": {
                "type": "raw",
                "value": raw_value
            }
        }

def parse_dice(token: str) -> dict:

    token = token.lower().strip()

    amount, sides = token.split("d")
    
    if amount == "":
        amount = 1
    else:
        amount = int(amount)
    
    if not sides == "f":   
        sides = int(sides)

    return {
        "type": "dice",
        "amount": amount,
        "sides": sides
    }


def attach_function(node: dict, func: dict) -> dict:

    func["arguments"] = [node]

    return func


def parse_command(command: str) -> dict:

    command = re.sub(r"\s+", "", command)

    elements = re.split(r"([+\-*/])", command)

    parsed_elements = []

    for element in elements:

        if not element:
            continue

        if element in "+-*/":
            parsed_elements.append(element)
            continue

        parts = element.split("|")

        current = None

        for part in parts:

            if re.match(pt_dice, part):

                current = parse_dice(part)

            elif ":" in part:

                func = parse_function(part)

                current = attach_function(current, func)

        parsed_elements.append(current)

    # Sem operadores
    if len(parsed_elements) == 1:
        return parsed_elements[0]

    # Com operadores
    root = {
        "name": parsed_elements[1],
        "arguments": [
            parsed_elements[0],
            parsed_elements[2]
        ]
    }

    index = 3

    while index < len(parsed_elements):

        operator = parsed_elements[index]
        operand = parsed_elements[index + 1]

        # Mesmo operador → agrega argumentos
        if operator == root["name"]:

            root["arguments"].append(operand)

        else:
            # Operador diferente → cria novo nó
            root = {
                "name": operator,
                "arguments": [
                    root,
                    operand
                ]
            }

        index += 2

    return root


if __name__ == "__main__":

    tests = [
        "5d6|kh:3",
        "5d6|kh:3|cn:>4",
        "1d4 + 5d6|kh:3|cn:>4",
        "1d4 + 2d6 + 3d8",
        "1d4 + 5d6|kh:3 + 3d10|kl:2"
    ]

    for test in tests:

        print("\n" + "=" * 80)
        print(test)
        print("=" * 80)

        pprint(parse_command(test), sort_dicts=False)