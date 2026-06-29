# parser.py
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

import re

pt_dice = r'^(?:[1-9][0-9]?)?d(?:f|[1-9][0-9]{0,2})+$'
pt_int  = r'^[0-9]+$'

POOL_FUNCTIONS = {"kh", "kl", "ex", "rr"}

KNOWN_FUNCTIONS = POOL_FUNCTIONS | {"cn"}
ALL_FUNCTIONS   = KNOWN_FUNCTIONS | {"mr"}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _node_produces_pool(node: dict) -> bool:

    if node is None:
        return False
    type = node.get("type")
    if type == "dice":
        return True
    if type == "integer":
        return False
    name = node.get("name")
    # kh/kl/ex/rr maintain pool; cn and operators produce scalar
    return name in POOL_FUNCTIONS


def validate_node(node: dict) -> str | None:
    """
    Returns a message if invalid, None if valid.
    """
    if node is None:
        return "Empty or missing node"

    type = node.get("type")
    
    if type == "dice":
        qty   = node.get("amount")
        faces = node.get("sides")

        if qty is None or faces is None:
            return "Invalid dice node: missing amount or sides"
        
        if not isinstance(qty, int) or qty < 1:
            return f"Invalid dice quantity: {qty}"
        
        if not (isinstance(faces, int) or faces == "f"):
            return f"Invalid dice faces: {faces}"
        
        return None
    
    if type == "integer":
        if not isinstance(node.get("value"), int):
            return f"Invalid integer value: {node.get('value')}"
        
        return None

    name = node.get("name")
    
    if name in {"+", "-", "*", "/"}:
        args = node.get("arguments", [])
        
        if not args:
            return f"Operator '{name}' has no arguments"

        for arg in args:
            if arg is None:
                return f"Operator '{name}' has a None argument"
            
            if isinstance(arg, dict) and arg.get("name") in POOL_FUNCTIONS:
                inner = (arg.get("arguments") or [None])[0]
                
                if inner is not None and inner.get("type") == "integer":
                    fn = arg["name"]
                    
                    return f"'{fn}' requires a dice argument, use 'NdX | {fn}:...' not 'N | {fn}:...'"
                    
                if inner is None:
                    fn = arg["name"]
                    
                    return f"'{fn}' requires a dice argument, use 'NdX | {fn}:...'"
                    

            err = validate_node(arg)
            if err:
                return err

        return None

    
    if name not in ALL_FUNCTIONS:
        return f"Unknown function: '{name}'"
    
    # detected here when it appears as an argument to an operator or another function

    args = node.get("arguments", [])
    if not args:
        return f"Function '{name}' has no arguments"

    arg = args[0]

    if arg is None:
        return f"'{name}' has no dice argument"

    
    if isinstance(arg, dict) and arg.get("name") == "mr":
        return f"'mr' must be the last element — cannot be used as argument to '{name}'"

    
    if name == "mr":
        
        if isinstance(arg, dict) and arg.get("type") == "integer":
            return "'mr' requires a dice argument, not a literal integer"

        selector = node.get("selector", {})
        val = selector.get("value")
        if val is None or not isinstance(val[0], int) or val[0] < 1:
            return f"'mr' repetition count must be a positive integer, got {val}"

        return validate_node(arg)

    
    if not _node_produces_pool(arg):
        return f"'{name}' requires a dice argument, got scalar, use 'NdX | {name}:...' not 'N | {name}:...'"
        

    err = validate_node(arg)
    if err:
        return err

    selector = node.get("selector", {})

    if name in ("kh", "kl"):
        val = selector.get("value")

        if val is None:
            f"'{name}' missing selector value"

        if not isinstance(val[0], int):
            return f"'{name}' selector value must be int, got {val[0]}"
        
        if val[0] < 1:
            return f"'{name}' value must be >= 1, got {val[0]}"

    if name == "cn":
        if selector.get("condition") is None:
            return "'cn' missing condition"
        
        if selector.get("value") is None:
            return "'cn' missing value"

    if name in ("ex", "rr"):
        if selector.get("condition") is None:
            return f"'{name}' missing condition"
        
        if selector.get("value") is None:
            return f"'{name}' missing value"

    return None

# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------

def parse_function(token: str) -> dict:
    name, raw_value = token.split(":", 1)
    name = name.strip()
    raw_value = raw_value.strip()

    if not raw_value:
        raise ValueError(f"Function '{name}' has no value after ':'")

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

    # Lista (11,12)
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

    # Operador relacional (>=, <=, !=, >, <, =)
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

    # Valor simples (inteiro)
    try:
        return {
            "name": name,
            "selector": {
                "condition": "=",
                "value": [int(raw_value)]
            }
        }
    except ValueError:
        # Valor bruto (fallback)
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

    if sides != "f":
        sides = int(sides)

    return {
        "type": "dice",
        "amount": amount,
        "sides": sides
    }


def parse_integer(token: str) -> dict:
    return {
        "type": "integer",
        "value": int(token)
    }


def attach_function(node: dict, func: dict) -> dict:
    """Encadeia uma função ao nó atual. node pode ser None quando o
    inteiro literal precede um pipe — a validação posterior captura isso."""
    func["arguments"] = [node]
    return func


def _elevate_mr(root: dict) -> dict:
    """
    If the root node is an arithmetic operator whose last argument is mr,

    it raises mr to the root, enclosing the entire expression.

    Example: {+: [5d6, mr(int(1))]} → mr(arg={+: [5d6, int(1)]})
    """
    if not isinstance(root, dict):
        return root

    if root.get("name") not in {"+", "-", "*", "/"}:
        return root

    args = root.get("arguments", [])
    if not args:
        return root

    last = args[-1]
    if not isinstance(last, dict) or last.get("name") != "mr":
        return root

    # O token que o mr "capturou" vira o último elemento real do operador
    mr_inner = last["arguments"][0]
    new_root = dict(root)
    new_root["arguments"] = args[:-1] + [mr_inner]

    return {
        "name": "mr",
        "selector": last["selector"],
        "arguments": [new_root]
    }


def parse_command(command: str) -> dict:
    # Remove espaços
    command = re.sub(r"\s+", "", command)

    # Divide pelos operadores aritméticos, preservando-os
    elements = re.split(r"([+\-*/])", command)

    parsed_elements = []

    for element in elements:

        if not element:
            continue

        if element in "+-*/":
            parsed_elements.append(element)
            continue

        # Divide pelo pipe — cada parte é dado ou função
        parts = element.split("|")

        current = None

        for part in parts:
            if re.match(pt_dice, part):
                current = parse_dice(part)

            elif re.match(pt_int, part):
                current = parse_integer(part)

            elif ":" in part:
                func = parse_function(part)
                current = attach_function(current, func)

        parsed_elements.append(current)

    # Apenas um elemento
    if len(parsed_elements) == 1:
        return parsed_elements[0]

    # Monta árvore aritmética (esquerda para direita, sem precedência)
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
                "arguments": [root, operand]
            }

        index += 2

    node = _elevate_mr(root)    
    err = validate_node(node)
     
    if err:
        raise ValueError(err)
    
    
    return node