# regexpatterns.py
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

# Validation Patterns

pt_split = r'(:|\||\.\.|<|>|,)'
pt_integer = r'^[1-9][0-9]{0,2}+$'
pt_number = r'[1-9][0-9]{0,2}'
pt_operator = r'^[+\-]+$'
pt_pipe = r'^\|+$'
# pt_dice = r'^[1-9][0-9]?d(f|[1-9][0-9]{0,2})+$'
pt_dice = r'^(?:[1-9][0-9]?)?d(?:f|[1-9][0-9]{0,2})+$'

pt_dice_prefix = r'[1-9][0-9]?d(?:f|[1-9][0-9]{0,2})'
pt_sufix = r'(?=\|[A-Za-z]{{2}}:|$)'

pt_ge_le = rf"[<>]{pt_number}"
pt_range = rf"{pt_number}\.\.{pt_number}"

pt_item = rf"(?:{pt_number}|{pt_ge_le}|{pt_range})"
pt_sep = rf"(?:,{pt_item})*"

pt_function = rf"^[a-zA-Z]{{2}}:{pt_item}{pt_sep}$"
pt_dice_func = rf"^(?:{pt_dice_prefix}\|)[a-zA-Z]{{2}}:{pt_item}{pt_sep}$"

pt_ex = rf"^(?:{pt_dice_prefix}\|)ex:{pt_item}{pt_sep}$"
pt_rr = rf"^(?:{pt_dice_prefix}\|)rr:{pt_item}{pt_sep}$"
pt_mr = rf"^(?:{pt_dice_prefix}\|)mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

pt_ex_b = rf"^ex:{pt_item}{pt_sep}$"
pt_rr_b = rf"^rr:{pt_item}{pt_sep}$"
pt_mr_b = rf"^mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

# pt_cn = rf"^cn:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
# pt_st = rf"^st:(?:{pt_number})$"

pt_cn = rf"^cn:{pt_item}{pt_sep}$"


pt_kh = rf"^(?:{pt_dice_prefix}\|)kh:(?:{pt_number})$"
pt_kl = rf"^(?:{pt_dice_prefix}\|)kl:(?:{pt_number})$"

pt_kh_b = rf"^kh:(?:{pt_number})$"
pt_kl_b = rf"^kl:(?:{pt_number})$"