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

from .regexpatterns import (
    pt_cn, pt_kh, pt_kl, pt_ex, pt_integer, pt_pipe,
    pt_mr, pt_rr, pt_dice, pt_operator, pt_function,
    pt_kh_b, pt_kl_b, pt_ex_b, pt_rr_b,
)


# ── helpers de dados ──────────────────────────────────────────────────────────

def roll_dice(expression: str) -> tuple[list, str]:
    """Rola N dados de F faces. Retorna (resultados ordenados desc, log)."""
    n_str, f_str = re.split('d', expression)
    n = int(n_str) if n_str else 1

    if f_str == 'f':
        faces, low = 3, -1
    else:
        faces, low = int(f_str), 1

    results = sorted(
        [random.randint(low, faces) for _ in range(n)],
        reverse=True,
    )
    return results, f"{n}d{faces} = {results}"


def _parse_parameters(expression: str, pool: list) -> tuple[list, str]:
    """
    Extrai o grupo de valores-alvo a partir de uma sub-expressão de parâmetro.

    Formatos aceitos:
      < N        → valores ≤ N
      > N        → valores ≥ N
      N .. M     → valores entre N e M (inclusive)
      a, b, c   → lista explícita
    """
    parts = re.split(r'(:|\||\.\.|<|>|,)', expression)
    log = ''.join(p for p in parts if p)

    # Descarta separadores para pegar só os valores
    values = [p for p in parts if p not in ('', ':', '|', '..', '<', '>', ',')]

    if len(values) == 2:
        op, n = values[0], int(values[1])
        if op == '<':
            return [e for e in pool if e <= n], log
        if op == '>':
            return [e for e in pool if e >= n], log

    if len(values) == 3 and parts[parts.index(values[0]) + 1 if values[0] in parts else 1] == '..':
        lo, hi = int(values[0]), int(values[2])
        return [e for e in pool if lo <= e <= hi], log

    return [int(v) for v in values], log


def _parse_parameters(raw: str, pool: list) -> tuple[list, str]:
    """
    Deriva grupo-alvo e log a partir da parte de parâmetros de um comando.
    raw é tudo após o primeiro separador ':' ou '|'.
    """
    parts = re.split(r'(\.\.|<|>|,)', raw)
    log = raw  # exibe como veio

    tokens = [p.strip() for p in parts if p.strip() not in ('', '..', '<', '>', ',')]

    # < N  ou  > N
    if len(parts) >= 3 and parts[1] in ('<', '>'):
        n = int(tokens[-1])
        if parts[1] == '<':
            return [e for e in pool if e <= n], log
        return [e for e in pool if e >= n], log

    # N .. M
    if '..' in parts:
        lo, hi = int(tokens[0]), int(tokens[-1])
        return [e for e in pool if lo <= e <= hi], log

    # lista explícita
    return [int(t) for t in tokens], log


def setup_parameters(parameters: list, pool: list) -> tuple[list, str]:
    """
    Versão compatível com o código original.
    `parameters` é a fatia de elements[2:] após split por separadores.
    """
    log = ''.join(p for p in parameters if p)
    clean = [p for p in parameters if p not in ('', ',')]

    if len(clean) == 3 and clean[1] in ('<', '>'):
        n = int(clean[2])
        if clean[1] == '<':
            return [e for e in pool if e <= n], log
        return [e for e in pool if e >= n], log

    if len(clean) == 3 and clean[1] == '..':
        lo, hi = int(clean[0]), int(clean[2])
        return [e for e in pool if lo <= e <= hi], log

    return [int(v) for v in clean], log


# ── operações de dado ─────────────────────────────────────────────────────────

def keep_subset(command: str, keep: int, pool: list,
                dice: str | None) -> tuple[list, str]:
    """Mantém os N maiores (kh) ou N menores (kl) de um pool."""
    dice_log = f"{dice} = {pool}" if dice else str(pool)

    if command in ('highest', 'kh'):
        subroll = pool[:keep]
        text = 'Highest'
    else:  # lowest / kl
        subroll = pool[-keep:]
        text = 'Lowest'

    return subroll, f"{text} {keep} in {dice_log} = {subroll}"


def explode(pool: list, faces: str, parameters: list,
            log: str) -> tuple[list, str]:
    """Rola dados extras para cada valor que caia no grupo-alvo (recursivo)."""
    group, param_log = setup_parameters(parameters, pool)
    dice = f"1d{faces}"
    counter = 0

    def _roll_extra(value_log):
        nonlocal counter, log
        if counter >= 50:
            return
        extra, extra_log = roll_dice(dice)
        pool.append(extra[0])
        log = f"{log}, extra {extra_log}"
        if extra[0] in group:
            counter += 1
            _roll_extra(extra_log)
        else:
            counter = 0

    for element in list(pool):
        if element in group:
            _roll_extra(log)

    pool.sort(reverse=True)
    return pool, f"Explode {param_log} in {log} = {pool}"


def reroll(pool: list, parameters: list, faces: str,
           log: str) -> tuple[list, str]:
    """Rerola valores que caiam no grupo-alvo (uma vez cada)."""
    group, param_log = setup_parameters(parameters, pool)
    dice = f"1d{faces}"
    new_pool = []

    for element in pool:
        if element in group:
            extra, extra_log = roll_dice(dice)
            new_pool.append(extra[0])
            log = f"{log}, reroll {element} = {extra}"
        else:
            new_pool.append(element)

    return new_pool, f"Reroll {param_log} in {log} = {new_pool}"


def count_in(expression: str, pool: list) -> tuple[str, str]:
    """Conta quantos valores do pool satisfazem a condição."""
    parts = re.split(r'(:|\||\.\.|<|>|,)', expression)
    command = parts[0]
    parameters = parts[2:]

    group, param_log = setup_parameters(parameters, pool)

    if command in ('check', 'ch'):
        values, label = [sum(pool)], 'Check'
    else:
        values, label = pool, 'Count'

    total = str(sum(1 for v in values if v in group))
    return total, f"{label} {param_log} = {total}"


def multiroll(expression: str) -> tuple[list, str]:
    """Rola o mesmo dado N vezes e retorna todos os pools."""
    parts = re.split(r'(:|\||\.\.|<|>)', expression)
    times = int(parts[4])
    dice_expr = parts[0]

    results = [roll_dice(dice_expr)[0] for _ in range(times)]
    return results, f"Multiroll {times} x {dice_expr}"


# ── montagem de comando ───────────────────────────────────────────────────────

def _next_is_function(commands: list, index: int) -> bool:
    return (index + 2 < len(commands)
            and re.match(pt_function, commands[index + 2]))


def address_commands(commands: list, testing: bool = False) -> list:
    """
    Processa a lista de tokens e retorna [True, resultado_numérico, log].
    """
    result_parts: list[str] = []
    log_parts: list[str] = []
    pool: list | None = None
    operation: str | None = None
    working_dice: str | None = None

    if testing:
        pool = commands[0]

    def _flush_pool_with_op():
        """Se há operação pendente e um pool, resolve e limpa ambos."""
        nonlocal pool, operation
        if operation and pool:
            val = f"{sum(pool)}"
            result_parts.append(f"{operation} {val}")
            pool = None
            operation = None

    for index, token in enumerate(commands):

        total = ''
        log = ''

        # ── dado simples: NdF ────────────────────────────────────────────────
        if re.match(pt_dice, token):
            roll, log = roll_dice(token)
            working_dice = token

            if operation:
                prev = sum(pool) if pool else None
                total = (f"{prev} {operation} {sum(roll)}"
                         if prev is not None else f"{operation} {sum(roll)}")
                log = (f"= {prev} {operation} {log} = {sum(roll)}"
                       if prev is not None else f"{operation} {log} = {sum(roll)}")
                pool = None
                operation = None
            else:
                pool = roll

        # ── inteiro ──────────────────────────────────────────────────────────
        elif re.match(pt_integer, token):
            total = token
            log = token
            if operation:
                prev = sum(pool) if pool else None
                total = (f"{prev} {operation} {token}"
                         if prev is not None else f"{operation} {token}")
                log = f"= {total}"
                pool = None
                operation = None

        # ── operador + / - ───────────────────────────────────────────────────
        elif re.match(pt_operator, token):
            if pool:
                result_parts.append(str(sum(pool)))
                log = f"= {sum(pool)}"
                pool = None
            operation = token

        # ── explode com dado próprio: NdF|ex:… ───────────────────────────────
        elif re.match(pt_ex, token):
            parts = re.split(r'(:|\||\.\.|<|>|,)', token)
            parameters = parts[4:]
            _, faces = re.split('d', parts[0])
            dice_pool, dice_log = roll_dice(parts[0])
            working_dice = parts[0]
            roll, log = explode(dice_pool, faces, parameters, dice_log)
            pool = roll
            if operation and not _next_is_function(commands, index):
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"
                pool = None
                operation = None

        # ── explode sobre pool existente: ex:… ───────────────────────────────
        elif re.match(pt_ex_b, token):
            parts = re.split(r'(:|\||\.\.|<|>)', token)
            _, faces = re.split('d', working_dice)
            roll, log = explode(pool, faces, parts[2:], str(pool))
            pool = roll
            if operation and not _next_is_function(commands, index):
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"
                pool = None
                operation = None

        # ── multiroll ────────────────────────────────────────────────────────
        elif re.match(pt_mr, token):
            if operation:
                raise ValueError('Multirolls cannot be added.')
            roll, log = multiroll(token)
            log_parts.append(log)
            return [True, roll, ' '.join(log_parts)]

        # ── reroll com dado próprio: NdF|rr:… ────────────────────────────────
        elif re.match(pt_rr, token):
            parts = re.split(r'(:|\||\.\.|<|>|,)', token)
            parameters = parts[4:]
            _, faces = re.split('d', parts[0])
            dice_pool, dice_log = roll_dice(parts[0])
            working_dice = parts[0]
            roll, log = reroll(dice_pool, parameters, faces, dice_log)
            pool = roll
            if operation and not _next_is_function(commands, index):
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"
                pool = None
                operation = None

        # ── reroll sobre pool existente: rr:… ────────────────────────────────
        elif re.match(pt_rr_b, token):
            parts = re.split(r'(:|\||\.\.|<|>)', token)
            _, faces = re.split('d', working_dice)
            roll, log = reroll(pool, parts[2:], faces, str(pool))
            pool = roll
            if operation and not _next_is_function(commands, index):
                total = f"{operation} {sum(roll)}"
                log = f"{operation} {log} = {sum(roll)}"
                pool = None
                operation = None

        # ── keep highest/lowest com dado próprio: NdF|kh:N ───────────────────
        elif re.match(pt_kh, token) or re.match(pt_kl, token):
            parts = re.split(r'(:|\||\.\.|<|>)', token)
            dice_pool, _ = roll_dice(parts[0])
            working_dice = parts[0]
            roll, log = keep_subset(parts[2], int(parts[4]), dice_pool, parts[0])
            if operation and not _next_is_function(commands, index):
                prev = sum(pool) if pool else None
                total = (f"{prev} {operation} {sum(roll)}"
                         if prev is not None else f"{operation} {sum(roll)}")
                log = (f"= {prev} {operation} {log} = {sum(roll)}"
                       if prev is not None else f"{operation} {log} = {sum(roll)}")
                pool = None
                operation = None
            else:
                pool = roll

        # ── keep highest/lowest sobre pool existente: kh:N ───────────────────
        elif re.match(pt_kh_b, token) or re.match(pt_kl_b, token):
            parts = re.split(r'(:|\||\.\.|<|>)', token)
            if pool:
                roll, log = keep_subset(parts[0], int(parts[2]), pool, None)
                if operation and not _next_is_function(commands, index):
                    total = f"{operation} {sum(roll)}"
                    log = f"{operation} {log} = {sum(roll)}"
                    pool = None
                    operation = None
                else:
                    pool = roll

        # ── count ────────────────────────────────────────────────────────────
        elif re.match(pt_cn, token):
            values = pool if pool else [eval(' '.join(result_parts))]
            total, log = count_in(token, values)
            pool = None
            result_parts.clear()

        if total:
            result_parts.append(total)
        if log:
            log_parts.append(log)

    if pool:
        result_parts.append(str(sum(pool)))

    final_expr = ' '.join(result_parts)
    return [True, eval(final_expr), ' '.join(log_parts)]


# ── validação ────────────────────────────────────────────────────────────────

_ALL_PATTERNS = (
    pt_dice, pt_integer, pt_operator,
    pt_ex, pt_rr, pt_kh, pt_kl,
    pt_ex_b, pt_rr_b, pt_kh_b, pt_kl_b,
    pt_cn,
)

_BOUND_PATTERNS = (pt_ex_b, pt_rr_b, pt_kh_b, pt_kl_b)


def validate_elements(commands: list) -> list | None:
    """Retorna [False, None, mensagem] se inválido, None se válido."""
    if not commands:
        return [False, None, "Empty Command"]

    for index, element in enumerate(commands):
        if not any(re.match(p, element) for p in _ALL_PATTERNS):
            return [False, None, f"Sintaxe Error: {element}"]

        if any(re.match(p, element) for p in _BOUND_PATTERNS):
            prev = commands[index - 1]
            if re.match(pt_integer, prev) or re.match(pt_operator, prev):
                return [False, None, f"Sintaxe Error: {element} not preceded"]

    return None


# ── ponto de entrada ──────────────────────────────────────────────────────────

def execute_command(commands: str) -> list:
    """
    Recebe uma string de expressão (digitada ou montada pelos botões),
    normaliza, tokeniza, valida e executa.
    """
    commands = re.sub(r' ', '', commands)
    tokens = re.split(r'(\+|\-|\|)', commands)

    fixed = []
    for i, token in enumerate(tokens):
        if re.match(pt_pipe, token):
            continue

        # Funde "NdF" + "|" + "função" em um único token "NdF|função"
        if (i < len(tokens) - 2
                and re.match(pt_dice, token)
                and re.match(pt_function, tokens[i + 2])
                and not re.match(pt_cn, tokens[i + 2])):
            fixed.append(f"{token}|{tokens[i + 2]}")
            continue

        # Pula a função que já foi fundida acima
        if (i >= 2
                and re.match(pt_function, token)
                and re.match(pt_dice, tokens[i - 2])
                and not re.match(pt_cn, token)):
            continue

        fixed.append(token)

    validation = validate_elements(fixed)
    if validation:
        return validation

    return address_commands(fixed)