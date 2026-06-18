# rollarea.py
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


from gi.repository import Gtk

from .dicearea import DiceArea
from .infoarea import InfoArea
from .advancedmode import AdvancedMode


# Mapeamento canônico: chave → (atributo do botão, label da face)
# A chave 'modifier' é especial: representa o bônus/penalidade numérico.
DICE_MAP = {
    'df':   ('_df_button',   'df'),
    'd4':   ('_d4_button',   'd4'),
    'd6':   ('_d6_button',   'd6'),
    'd8':   ('_d8_button',   'd8'),
    'd10':  ('_d10_button',  'd10'),
    'd12':  ('_d12_button',  'd12'),
    'd20':  ('_d20_button',  'd20'),
    'd100': ('_d100_button', 'd100'),
}


def _empty_command() -> dict:
    """Retorna um dicionário de comando zerado."""
    command = {key: 0 for key in DICE_MAP}
    command['modifier'] = 0
    return command


def _assemble_expression(command: dict) -> str:
    """Monta a string de expressão a partir do dicionário de comando."""
    parts = []

    for key, (_, label) in DICE_MAP.items():
        count = command[key]
        if count:
            parts.append(f"{count}{label}")

    modifier = command['modifier']
    if modifier > 0:
        parts.append(f"+ {modifier}")
    elif modifier < 0:
        parts.append(f"- {abs(modifier)}")

    return ' + '.join(p for p in parts if not p.startswith(('+ ', '- '))) \
           + (' ' + ' '.join(p for p in parts if p.startswith(('+ ', '- ')))
              if any(p.startswith(('+ ', '- ')) for p in parts) else '') \
           if parts else ''


def _assemble_expression(command: dict) -> str:
    """Monta a string de expressão a partir do dicionário de comando."""
    dice_parts = []
    modifier_part = ''

    for key, (_, label) in DICE_MAP.items():
        count = command[key]
        if count:
            dice_parts.append(f"{count}{label}")

    modifier = command['modifier']
    if modifier > 0:
        modifier_part = f"+ {modifier}"
    elif modifier < 0:
        modifier_part = f"- {abs(modifier)}"

    parts = dice_parts
    if modifier_part:
        parts = dice_parts + [modifier_part]

    return ' + '.join(parts).replace('+ -', '-')


@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/RollArea.ui')
class RollArea(Gtk.Box):
    __gtype_name__ = 'RollArea'

    _results = Gtk.Template.Child()
    _stack = Gtk.Template.Child()
    _dice_area = Gtk.Template.Child()
    _info_area = Gtk.Template.Child()
    _display = Gtk.Template.Child()
    _mode_button = Gtk.Template.Child()
    _roll_button = Gtk.Template.Child()
    _clear_button = Gtk.Template.Child()
    _adaptable = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._command = _empty_command()

        self._roll_button.connect("clicked", self._do_roll)
        self._clear_button.connect("clicked", self._clear_display)
        self._mode_button.connect("toggled", self._change_mode)

        # Conecta cada botão de dado usando o DICE_MAP
        for key, (btn_attr, _) in DICE_MAP.items():
            button = getattr(self._dice_area, btn_attr)
            button.connect("clicked", self._add_die, key)

        self._dice_area._plus_button.connect("clicked", self._add_modifier, +1)
        self._dice_area._minus_button.connect("clicked", self._add_modifier, -1)

        buffer = self._display.get_buffer()
        buffer.connect("inserted-text", self._reset_error_state)
        buffer.connect("deleted-text", self._reset_error_state)

        self._display.connect("activate", self._do_roll)
        self._display.connect("changed", self._button_activation)

        self._button_activation(self._display)

    # ── estado ──────────────────────────────────────────────────────────────

    def _reset_error_state(self, *args):
        if self._display.has_css_class("error"):
            self._display.remove_css_class("error")

    def _clear_display(self, _button):
        self._command = _empty_command()
        self._display.set_text("")
        self._results.set_text("?")

    def update_result(self, total):
        self._results.set_text(str(total))

    # ── modo básico: botões ──────────────────────────────────────────────────

    def _add_die(self, _button, die_key: str):
        self._command[die_key] += 1
        self._display.set_text(_assemble_expression(self._command))

    def _add_modifier(self, _button, delta: int):
        self._command['modifier'] += delta
        self._display.set_text(_assemble_expression(self._command))

    # ── alternância de modo ──────────────────────────────────────────────────

    def _change_mode(self, button):
        advanced = self._mode_button.get_active()

        if advanced:
            self._stack.set_visible_child(self._info_area)
            self._display.set_editable(True)
            self._display.set_can_focus(True)
            self._display.set_placeholder_text("Ex.: 2d6, 1d12+3, 2d20|kh:1")
            self._display.grab_focus()
        else:
            self._stack.set_visible_child(self._dice_area)
            self._display.set_editable(False)
            self._display.set_can_focus(False)
            self._display.set_placeholder_text('')
            self._clear_display(None)

    # ── roll ─────────────────────────────────────────────────────────────────

    def _do_roll(self, _button):
        self.get_root().application.do_roll()
        self._command = _empty_command()

    def _button_activation(self, display):
        self._roll_button.set_sensitive(bool(display.get_text().strip()))