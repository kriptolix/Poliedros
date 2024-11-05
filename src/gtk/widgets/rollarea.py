# window.py
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

from gi.repository import Adw
from gi.repository import Gtk

from ...roller import command_handler, parse_command


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/RollArea.ui')
class RollArea(Gtk.Box):
    __gtype_name__ = 'RollArea'

    _amount = Gtk.Template.Child()
    _dice = Gtk.Template.Child()
    _increment = Gtk.Template.Child()
    _roll_button = Gtk.Template.Child()
    _result = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.dice_list = Gtk.StringList.new()
        self.amount_list = Gtk.StringList.new()
        self.buffer = self._increment.get_buffer()

        for dice in ("d4", "d6", "d8", "d10", "d12", "d20", "d100"):
            self.dice_list.append(dice)

        for amount in range(1, 13):
            self.amount_list.append(f"{amount}")

        self._dice.set_model(self.dice_list)
        self._amount.set_model(self.amount_list)

        # self._roll_button.connect("clicked", self._assemble_command)
        self._roll_button.connect("clicked", self._test)
        # self.buffer.connect("inserted-text", self._limit_input)

    def _update_result(self, results):
        self._result.set_text(results)

    def _assemble_command(self, button):

        dice_pos = self._dice.get_selected()
        dice = self.dice_list.get_string(dice_pos)

        amount_pos = self._amount.get_selected()
        amount = self.amount_list.get_string(amount_pos)

        increment = self._increment.get_text()

        command = f"{amount}{dice}{increment}"

        print(command)

        results = command_handler(command)

        self._update_result(results)

    def _limit_input(self, buffer, position, chars, n_chars):
        
        print(chars)

    def _test(self, button):
        input_command = self._increment.get_text()
        results = parse_command(input_command)
        # results = command_handler(input_command)
        print(results)