import re
from pprint import pprint

pt_dice = r'^(?:[1-9][0-9]?)?d(?:f|[1-9][0-9]{0,2})+$'

def parse_function(token: str) -> dict:
    name, raw_value = token.split(":", 1)
    raw_value = raw_value.strip()

    # Range (3..5)
    if ".." in raw_value:
        start, end = raw_value.split("..")

        return {
            "name": name,
            "selector": {
                "condition": "..",
                "value": [int(start), int(end)]
            }
        }
    
    
    if "," in raw_value:
        values = [v.strip() for v in raw_value.split(",")]

        parsed = []
        for v in values:
            try:
                parsed.append(int(v))
            except ValueError:
                parsed.append(v)

        return {
            "name": name,
            "selector": {
                "condition": "in",
                "value": parsed
            }
        }
    
    match = re.match(r"(>=|<=|!=|>|<|=)(.+)", raw_value)

    if match:
        op = match.group(1)
        value = match.group(2).strip()

        try:
            value = int(value)
        except ValueError:
            pass

        return {
            "name": name,
            "selector": {
                "condition": op,
                "value": [value]
            }
        }
    
    try:
        return {
            "name": name,
            "selector": {
                "condition": "=",
                "value": [int(raw_value)]
            }
        }

    # Valor bruto
    except ValueError:
        return {
            "name": name,
            "selector": {
                "condition": "raw",
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

    
    if len(parsed_elements) == 1:
        return parsed_elements[0]
    
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
        
        if operator == root["name"]:

            root["arguments"].append(operand)

        else:            
            root = {
                "name": operator,
                "arguments": [
                    root,
                    operand
                ]
            }

        index += 2

    print("root: ", root)
    return root