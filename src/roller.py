# roller.py
#
# Copyright 2024 k
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import re
import operator

from .parser import parse_command

def roll_dice(amount: int, sides: int | str) -> dict:    

    if sides == "f":
        sides = 3
        scope = [-1, 1]
    else:        
        scope = [1, sides]

    rolls = []

    for _ in range(amount):
        rolls.append(random.randint(scope[0], scope[1]))

    rolls.sort(reverse=True)

    log = {
        "type": "dice",        
        "amount": amount,
        "sides": sides,
        "rolls": rolls,
        "result": sum(rolls)
    }

    print("roll dice log: ", log) 
    return log


def count_in(pool: list, selector: dict) -> dict:
    """
    returns the number of elements that meet the criterion        
    """
    def _compare(op):

        value = selector["value"]
        return sum(1 for x in pool if op(x, value))
    ##

    sorted_pool = sorted(pool, reverse=True)

    rule_type = selector["type"]    
       
    if rule_type == "number":
        value = selector["value"]
        result = sorted_pool.count(value)        
    
    if rule_type == "gt":
        result = _compare(operator.gt)        

    if rule_type == "lt":
        result = _compare(operator.lt)

    if rule_type == "ge":
        result = _compare(operator.ge)        

    if rule_type == "le":
        result = _compare(operator.le)              
    
    if rule_type == "range":

        a = selector["from"]
        b = selector["to"]
        value = f"{a} to {b}"

        result = sum(1 for x in pool if a <= x <= b)        
    
    log = {
            "type": "cn",
            "condition": "range",
            "value": value,
            "input": sorted_pool,
            "result": result
        }

    return log

    

       

    


def keep_subset(command: str, keep: int, pool: list, dice: str | None) -> list:

    dice_log = f"{pool}"

    if dice:
        dice_log = f"{dice} = {pool}"

    match command:
        case "highest" | "kh":
            subroll = pool[:keep]
            excluded = pool[len(subroll):]
            excluded.insert(0, subroll)
            text = "Highest"

        case "lowest" | "kl":
            subroll = pool[-keep:]
            excluded = pool[:-len(subroll)]
            excluded.append(subroll)
            text = "Lowest"

    total = subroll
    log = f"{text} {keep} in {dice_log} = {subroll}"

    return [total, log]


def explode(pool: list, faces: str, parameters: list, log: str) -> list:

    def _recursive_roll(dice, group):

        nonlocal counter
        nonlocal log

        if counter >= 50:
            return

        extended_roll, extended_log = roll_dice(dice)

        pool.append(extended_roll[0])
        log = f"{log}, extra {extended_log}"

        if extended_roll[0] in group:
            counter = counter + 1
            _recursive_roll(dice, group)
            return

        counter = 0
    ##

    command = "Explode"

    group, parameter_log = setup_parameters(parameters, pool)

    counter = 0

    dice = f"1d{faces}"

    initial_pool = pool

    for element in initial_pool:
        if element in group:

            _recursive_roll(dice, group)

    pool.sort(reverse=True)

    total = pool
    log = f"{command} {parameter_log} in {log} = {pool}"

    return [total, log]


def reroll(pool: list, parameters: list, faces: str, log: str) -> list:

    command = "Reroll"

    group, parameter_log = setup_parameters(parameters, pool)

    dice = f"1d{faces}"

    extended_pool = []

    for element in pool:
        if element in group:
            extended_roll, extended_log = roll_dice(dice)

            extended_pool.append(extended_roll[0])
            log = f"{log}, reroll {element} = {extended_roll}"
            continue

        extended_pool.append(element)

    total = extended_pool
    log = f"{command} {parameter_log} in {log} = {total}"

    # print("total, log reroll:", total, log)

    return [total, log]


def multiroll(expression: str) -> list:

    extended_roll = []

    elements = re.split(r'(:|\||\.\.|<|>)', expression)
    command = "Multiroll"

    group = int(elements[4])

    # print("elements: ", elements)

    for _ in range(group):

        pool, log = roll_dice(elements[0])
        extended_roll.append(pool)

    total = extended_roll
    log = f"{command} {group} x {elements[0]}"

    # print(total, log)

    return [total, log]


def extract_dice(node, out=None):
    if out is None:
        out = {}

    if isinstance(node, dict):
        if node.get("type") == "dice":
            key = f"d{node['sides']}"
            out.setdefault(key, []).extend(node.get("rolls", []))

        for v in node.values():
            extract_dice(v, out)

    elif isinstance(node, list):
        for item in node:
            extract_dice(item, out)

    return out


FUNCTIONS = {
    "kh": keep_subset,
    "kl": keep_subset,
    "cn": count_in,
    "ex": explode,
    "rr": reroll,
    "mr": multiroll,
}

def _eval(node: dict) -> dict:
    
    if node.get("type") == "dice":

        result = roll_dice(
            amount=node["amount"],
            sides=node["sides"]
        )
        # print("dice results: ", result )
        return result        

    if node.get("type") == "integer":

        return {
            "type": "integer",
            "value": node["value"]
        }
   
    if node["name"] in {"+", "-", "*", "/"}:

        values = []
        logs = []

        for arg in node["arguments"]:

            # print("args", arg)

            v = _eval(arg)
            values.append(v["result"])
            logs.append(v)

        if node["name"] == "+":

            result = sum(values)

        elif node["name"] == "-":

            result = values[0]
            for v in values[1:]:
                result -= v

        '''
        elif node["name"] == "*":

            result = values[0]
            for v in values[1:]:
                result *= v

        elif node["name"] == "/":

            result = values[0]
            for v in values[1:]:
                result /= v
        '''

        return {
            "type": "operator",
            "op": node["name"],
            "children": logs,
            "result": result
        }

    arg_result, arg_log = _eval(node["arguments"][0])    

    if node["name"] == "cn":

        log = count_in(
            arg_result,
            node["condition"],
            node["value"]
        )

    else:
        raise ValueError(node)

    return {
        "type": "function",
        "name": node["name"],
        "value": node.get("value"),
        "condition": node.get("condition"),
        "child": arg_log,
        "result": result,
        "log": log
    }


def _flatten_log(node: dict) -> str:

    if node["type"] == "dice":
        
        return f'{node["amount"]}d{node["sides"]} = {node["rolls"]} = {node["result"]}'

    if node["type"] == "integer":
        return str(node["value"])

    if node["type"] == "operator":

        parts = [
            _flatten_log(child)
            for child in node["children"]
        ]

        return f" {node['op']} ".join(parts)

    if node["type"] == "function":

        child = _flatten_log(node["child"])

        if node["name"] in {"kh", "kl"}:
            return f"{node['name']}({child}, {node['value']})"

        if node["name"] == "cn":
            return f"cn({child} {node['condition']} {node['value']})"

        return f"{node['name']}({child})"


def address_commands(node: dict) -> dict:
    log_tree = _eval(node) 

    print("log tree: ", log_tree)   

    return {
        "result": log_tree.get("result"),
        "log": _flatten_log(log_tree)
    }


def validate_node(node: dict) -> list | None:
    """
    Retorna:
        [False, None, message] se inválido
        None se válido
    """

    if not node:
        return [False, None, "Empty Command"]

    
    if node.get("type") == "dice":

        qty = node.get("amount")
        faces = node.get("sides")

        if qty is None or faces is None:
            return [False, None, "Invalid dice node"]

        if not isinstance(qty, int) or qty < 1:
            return [False, None, f"Invalid dice qty: {qty}"]

        if not (isinstance(faces, int) or faces == "f"):
            return [False, None, f"Invalid dice faces: {faces}"]

        return None

    
    if node.get("type") == "integer":

        if not isinstance(node.get("value"), int):
            return [False, None, f"Invalid integer: {node.get('value')}"]

        return None

    
    if node.get("name") in {"+", "-", "*", "/"}:

        args = node.get("arguments", [])

        if not args:
            return [False, None, f"Operator {node['name']} missing arguments"]

        for arg in args:
            err = validate_node(arg)
            if err:
                return err

        return None

    
    name = node.get("name")

    if not name:
        return [False, None, "Missing function name"]

    args = node.get("arguments", [])

    if not args:
        return [False, None, f"Function {name} missing argument"]

    
    for arg in args:
        err = validate_node(arg)
        if err:
            return err

    
    if name in {"kh", "kl"}:

        if node.get("value") is None:
            return [False, None, f"{name} missing value"]

        if not isinstance(node["value"], int):
            return [False, None, f"{name} value must be int"]

    if name == "cn":

        if node.get("condition") is None:
            return [False, None, "cn missing condition"]

        if node.get("value") is None:
            return [False, None, "cn missing value"]

    return None


def execute_command(commands: str) -> list:

    node = parse_command(commands)

    validation = validate_node(node)

    if validation:
        return validation

    result = address_commands(node)

    print("node: ", node)
    print("result final: ", result)

    return [True, result.get("result"), result.get("log")]
