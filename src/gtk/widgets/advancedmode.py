# AdvancedMode.py
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


from gi.repository import Gtk, Adw

from .dicearea import DiceArea


@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/AdvancedMode.ui')
class AdvancedMode(Gtk.Box):
    __gtype_name__ = 'AdvancedMode'

    _display = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self._terms = ["lowest", "highest", "count", "explode"]

        buffer = self._display.get_buffer()

        buffer.connect("inserted-text", self._auto_complete)
        buffer.connect("deleted-text", self._auto_complete)

        self._display.connect("activate", self._do_roll)

    def _do_roll(self, button):

        application = self.get_root().application
        application.do_roll()
        self._command = [0, 0, 0, 0, 0, 0, 0]

    def _auto_complete(self, *args):

        text = self._display.get_text()

        for term in self._terms:
            if term == text:
                self._insert_widget(term)

    def _insert_widget(self, term):

        button = Gtk.Button.new()

        match term:
            case "lowest":
                button.set_label("lowest")
                self.prepend(button)
