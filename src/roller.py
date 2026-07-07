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
import operator as op_module
from gettext import gettext as _


def roll_dice(amount: int, sides: int | str) -> dict:
    if sides == "f":       
        scope = [-1, 1]
    else:
        scope = [1, sides]

    rolls = []
    for _ in range(amount):
        rolls.append(random.randint(scope[0], scope[1]))

    rolls.sort(reverse=True)

    return {
        "type": "dice",
        "amount": amount,
        "sides": sides,
        "rolls": rolls,
        "result": sum(rolls)
    }


# ---------------------------------------------------------------------------
# Selectors
# ---------------------------------------------------------------------------

def apply_selector(name: str, pool: list[int], selector: dict) -> list[int]:
    condition = selector.get("condition")
    values = selector.get("value", [])

    if name == "kh":
        return pool[:values[0]]

    if name == "kl":
        return pool[-values[0]:]

    if condition == "..":
        a, b = values
        return [x for x in pool if a <= x <= b]

    if condition == "in":
        return [x for x in pool if x in values]

    ops = {
        "=":  op_module.eq,
        "!=": op_module.ne,
        ">":  op_module.gt,
        ">=": op_module.ge,
        "<":  op_module.lt,
        "<=": op_module.le,
    }

    if condition in ops:
        v = values[0]
        fn = ops[condition]
        return [x for x in pool if fn(x, v)]

    raise ValueError(f"Unsupported selector condition: {condition}")


# ---------------------------------------------------------------------------
# Operações sobre pool
# ---------------------------------------------------------------------------

def count_in(pool: list[int], selector: dict) -> dict:
    filtered = apply_selector("cn", pool, selector)
    return {
        "type": "cn",
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "kept": filtered,
        "result": len(filtered),
    }


def keep_subset(name: str, pool: list[int], selector: dict) -> dict:
    labels = {"kh": "keep highest", "kl": "keep lowest", "kv": "keep"}
    kept = apply_selector(name, pool, selector)
    return {
        "type": name,
        "label": labels[name],
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "kept": kept,
        "result": sum(kept),   # escalar para aritmética
    }


def _check_selector(x: int, condition: str, values: list) -> bool:
    if condition == "=":   return x == values[0]
    if condition == ">":   return x > values[0]
    if condition == ">=":  return x >= values[0]
    if condition == "<":   return x < values[0]
    if condition == "<=":  return x <= values[0]
    if condition == "..":
        a, b = values
        return a <= x <= b
    if condition == "in":  return x in values
    return False


def process_reaction(pool: list[int], selector: dict, dice: dict, mode: str) -> list[int]:
    condition = selector["condition"]
    values = selector["value"]
    result = []

    for x in pool:
        if mode == "reroll" and not _check_selector(x, condition, values):
            result.append(roll_dice(1, dice["sides"])["rolls"][0])
        else:
            result.append(x)
            if mode == "explode" and _check_selector(x, condition, values):
                result.append(roll_dice(1, dice["sides"])["rolls"][0])

    return result


def explode_pool(pool: list[int], selector: dict, dice: dict) -> dict:
    rolled = process_reaction(pool, selector, dice, mode="explode")
    return {
        "type": "ex",
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "kept": rolled,
        "result": sum(rolled),   # escalar para aritmética
    }


def reroll_pool(pool: list[int], selector: dict, dice: dict) -> dict:
    rolled = process_reaction(pool, selector, dice, mode="reroll")
    return {
        "type": "rr",
        "condition": selector["condition"],
        "value": selector["value"],
        "input": pool,
        "kept": rolled,
        "result": sum(rolled),   # escalar para aritmética
    }


def multiroll(node: dict, times: int) -> dict:
    
    runs = []
    results = []
    for _ in range(times):
        run_log = _eval(node)
        runs.append(run_log)
        results.append(run_log["result"])
    return {
        "type": "mr",
        "times": times,
        "runs": runs,
        "result": results,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_pool(log: dict) -> list[int] | None:
    """
    Extracts the usable pool from any log node.
    """
    t = log.get("type")
    if t == "dice":
        return log.get("rolls")
    if t in ("kh", "kl", "ex", "rr"):
        return log.get("kept")
    return None


def _get_dice_node(log: dict) -> dict | None:
    """
    Traverses up the log chain to find the original dice node (for ex/rr).
    """
    if log.get("type") == "dice":
        return log
    child = log.get("child")
    if child:
        return _get_dice_node(child)
    return None


def _eval(node: dict) -> dict:
 
    if node.get("type") == "dice":
        return roll_dice(node["amount"], node["sides"])
  
    if node.get("type") == "integer":
        v = node["value"]
        return {"type": "integer", "value": v, "result": v}

    name = node.get("name")

    if name in {"+", "-", "*", "/"}:
        children_logs = []
        for arg in node["arguments"]:
            if arg is None:
                children_logs.append({"type": "integer", "value": 0, "result": 0})
                continue
            children_logs.append(_eval(arg))

        values = [c["result"] for c in children_logs]

        if name == "+":
            result = sum(values)
        elif name == "-":
            result = values[0]
            for v in values[1:]:
                result -= v
        elif name == "*":
            result = values[0]
            for v in values[1:]:
                result *= v
        elif name == "/":
            result = values[0]
            for v in values[1:]:
                result /= v

        return {
            "type": "operator",
            "op": name,
            "children": children_logs,
            "result": result
        }

    if name == "mr":
        times    = node["selector"]["value"][0]
        arg_node = node["arguments"][0]
        return multiroll(arg_node, times)

    # --- pool functions---
    arg_node = node["arguments"][0]
    arg_log = _eval(arg_node)

    pool = _get_pool(arg_log)
    dice_info = _get_dice_node(arg_log)

    selector = node["selector"]

    if name == "cn":
        fn_log = count_in(pool, selector)

    elif name == "kh":
        fn_log = keep_subset("kh", pool, selector)

    elif name == "kl":
        fn_log = keep_subset("kl", pool, selector)

    elif name == "ex":
        fn_log = explode_pool(pool, selector, dice_info)

    elif name == "rr":
        fn_log = reroll_pool(pool, selector, dice_info)

    else:
        raise ValueError(f"Unknown function: {name}")

    return {
        "type": name,
        "condition": selector.get("condition"),
        "value": selector.get("value"),
        "child": arg_log,
        "kept": fn_log.get("kept"),     # list for thread pool _get_pool
        "result": fn_log["result"],     
        "log": fn_log
    }


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------

def extract_dice_rolls(log_tree: dict, out: dict | None = None) -> dict:
    if out is None:
        out = {}
    if isinstance(log_tree, dict):
        if log_tree.get("type") == "dice":
            key = f"d{log_tree['sides']}"
            out.setdefault(key, []).extend(log_tree["rolls"])
        for v in log_tree.values():
            if isinstance(v, (dict, list)):
                extract_dice_rolls(v, out)
    elif isinstance(log_tree, list):
        for item in log_tree:
            extract_dice_rolls(item, out)
    return out


def _selector_str(condition: str, values: list) -> str:
    if condition == "..":
        return f"{values[0]}..{values[1]}"
    if condition == "in":
        return ",".join(str(v) for v in values)
    return f"{condition}{values[0]}"


def _child_summary(child_log: dict) -> str:
    
    t = child_log.get("type")
    if t == "dice":
        return f"{child_log['amount']}d{child_log['sides']} {child_log['rolls']}"
    if t in ("kh", "kl"):
        label = child_log["log"].get("label", t)
        return f"[{label} → {child_log['kept']}]"
    if t in ("ex", "rr"):
        return f"[{t} → {child_log['kept']}]"
    if t == "cn":
        return f"[cn → {child_log['result']}]"
    return str(child_log.get("result", "?"))


def _flatten_log(node: dict) -> str:

    t = node["type"]

    if t == "dice":
        return (
            f"{node['amount']}d{node['sides']} "
            f"→ {node['rolls']} "
            f"= {node['result']}"
        )

    if t == "integer":
        return str(node["value"])

    if t == "operator":
        parts = [_flatten_log(child) for child in node["children"]]
        return f" {node['op']} ".join(parts)

    if t == "cn":
        sel = _selector_str(node["condition"], node["value"])
        child = node["child"]
        return _("Count %(sel)s in %(child)s = %(result)s") % {
            "sel": sel,
            "child": _child_summary(child),
            "result": node["result"],
        }

    if t in ("kh", "kl"):
        sel_val = node["value"][0]
        label = "highest" if t == "kh" else "lowest"
        child = node["child"]
        kept = node["kept"]
        return _("Keep %(sel_val)s %(label)s in %(child)s → %(kept)s = %(total)s") % {
            "sel_val": sel_val,
            "label": label,
            "child": _child_summary(child),
            "kept": kept,
            "total": sum(kept),
        }

    if t == "ex":
        sel = _selector_str(node["condition"], node["value"])
        child = node["child"]
        kept = node["kept"]
        return _("Explode %(sel)s in %(child)s → %(kept)s = %(total)s") % {
            "sel": sel,
            "child": _child_summary(child),
            "kept": kept,
            "total": sum(kept),
        }

    if t == "rr":
        sel = _selector_str(node["condition"], node["value"])
        child = node["child"]
        kept = node["kept"]
        return _("Reroll %(sel)s in %(child)s → %(kept)s = %(total)s") % {
            "sel": sel,
            "child": _child_summary(child),
            "kept": kept,
            "total": sum(kept),
        }

    if t == "mr":
        times   = node["times"]
        results = node["result"]
        runs    = node["runs"]
        detail  = "\n  ".join(
            f"[{i+1}] {_flatten_log(r)}" for i, r in enumerate(runs)
        )
        return _("%(times)sx rolls:\n  %(detail)s\n= %(results)s") % {
            "times": times,
            "detail": detail,
            "results": results,
        }
    
    return _("[unknown type: %(type)s]") % {
        "type": t,
    }


def execute_command(node: dict) -> dict:
    
    log_tree = _eval(node)
    rolls = extract_dice_rolls(log_tree)

    return {
        "result": log_tree.get("result"),
        "log": _flatten_log(log_tree),
        "rolls": rolls
    }