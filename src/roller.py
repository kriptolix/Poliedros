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

    # print("roll dice log: ", log) 
    return log


def apply_selector(name: str, pool: list[int], selector: dict) -> list[int]:
    
    condition = selector.get("condition")
    values = selector.get("value", [])

    if name == "kh":
        keep = values[0]

        return pool[:keep]
    
    if name == "kl":
        keep = values[0]

        return pool[-keep:]

    if condition == "..":
        a, b = values
        return [x for x in pool if a <= x <= b]

    if condition == "in":
        return [x for x in pool if x in values]

    ops = {
        "=": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
    }

    if condition in ops:
        v = values[0]
        op = ops[condition]
        return [x for x in pool if op(x, v)] 

    raise ValueError(f"Unsupported selector condition: {condition}")

def count_in(pool: list[int], selector: dict) -> dict:
    filtered = apply_selector("cn", pool, selector)

    return {
        "type": "cn",
        "name": "Count",
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "result": len(filtered),
    }


def keep_subset(name: str, pool: list[int], selector: dict) -> dict:
    
    names = {
        "kh": "keep hight",
        "kl": "keep low",
        "kv": "keep"
    }
    
    filtered = apply_selector(name, pool, selector)

    return {
        "type": name,
        "name": names[name],
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "result": filtered,
    }


def process_reaction(pool: list[int], selector: dict, dice: dict, mode: str) -> list[int]:
    
    condition = selector["condition"]
    values = selector["value"]

    def check(x: int) -> bool:
        if condition == "=":
            return x == values[0]
        if condition == ">":
            return x > values[0]
        if condition == ">=":
            return x >= values[0]
        if condition == "<":
            return x < values[0]
        if condition == "<=":
            return x <= values[0]
        if condition == "..":
            a, b = values
            return a <= x <= b
        if condition == "in":
            return x in values
        return False

    result = []

    for x in pool:
        
        if mode == "reroll" and not check(x):
            # substitui dado inválido
            new_roll = roll_dice(1, dice["sides"])["rolls"][0]
            result.append(new_roll)

        else:
            result.append(x)

            if mode == "explode" and check(x):
                # adiciona novo dado extra
                new_roll = roll_dice(1, dice["sides"])["rolls"][0]
                result.append(new_roll)

    return result


def explode(pool: list[int], selector: dict, dice: dict) -> dict:

    '''
    Rerolls dice according to a condition, the result replaces the previous one
    '''
    processed = process_reaction(pool, selector, dice, mode="explode")

    return {
        "type": "explode",        
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "result": processed,
    }

def reroll(pool: list[int], selector: dict, dice: dict) -> dict:
    '''
    Rerolls dice according to a condition, the result is added the previous one
    '''
    processed = process_reaction(pool, selector, dice, mode="reroll")
    return {
        "type": "reroll",        
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "result": processed,
    }
    

def multiroll(dice:dict, times:int) -> dict:
    '''
    rolls the same group of dice multiple times
    '''
    pass


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

    arg_log = _eval(node["arguments"][0])

    print("arq_log: ", arg_log)    

    if node["name"] == "cn":

        log = count_in(
            arg_log.get("rolls"),
            node["selector"]
        )

    elif node["name"] == "kh":

        log = keep_subset(
            "kh",
            arg_log.get("rolls"),
            node["selector"]
        )

    elif node["name"] == "kl":

        log = keep_subset(
            "kl",
            arg_log.get("rolls"),
            node["selector"]
        )

    else:
        raise ValueError(node)

    return {
        "type":  node["name"],
        "condition": node["selector"].get("condition"),
        "value": node["selector"].get("value"),
        "child": arg_log,
        "result": log.get("result"),
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

    if node["type"] == "cn":

        condition = node["condition"]
        values = node["value"]        

        if condition == "..":
            selector = f"{values[0]}..{values[1]}"
        elif condition == "in":
            selector = f"{values} in "
        else:
            selector = f"{condition}{values[0]}"

        text = (
            f"Count {selector} "
            f"in {node['child']['amount']}d{node['child']['sides']} "
            f"{node['child']['rolls']} = {node['result']}"
        )

    if node["type"] in ("kh", "kl", "kv"):

        condition = node["condition"]
        values = node["value"]

        match node["type"]:
            case "kh":
                begin = f"Keep {values[0]} highest "

            case "kl":
                begin = f"Keep {values[0]} lowest "
            
            case "kkv":
                begin = f"Keep {condition}{values[0]} "

        text = (
            f"{begin}"
            f"in {node['child']['amount']}d{node['child']['sides']} "
            f"{node['child']['rolls']} = {node['result']}"
        )       
        
        print(text)
        return text      


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

        if node["selector"].get("value") is None:
            return [False, None, f"{name} missing value"]

        # if not isinstance(node["selector"].get("value"), int):
            # return [False, None, f"{name} value must be int"]

    if name == "cn":

        print(node)

        if node["selector"].get("condition") is None:
            return [False, None, "cn missing condition"]

        if node["selector"].get("value") is None:
            return [False, None, "cn missing value"]

    return None


def execute_command(commands: str) -> list:

    node = parse_command(commands)

    validation = validate_node(node)

    if validation:
        return validation

    result = address_commands(node)

    # print("node: ", node)
    print("result final: ", result)

    return [True, result.get("result"), result.get("log")]
