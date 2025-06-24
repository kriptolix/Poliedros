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


@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/AdvancedMode.ui')
class AdvancedMode(Gtk.Box):
    __gtype_name__ = 'AdvancedMode'

    _drop_function = Gtk.Template.Child()
    _parameters = Gtk.Template.Child()
    _add_function = Gtk.Template.Child()
    _amount = Gtk.Template.Child()
    _faces = Gtk.Template.Child()
    _add_number = Gtk.Template.Child()
    _add_dicepool = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.display = None

        function_pool = [0, 0, 0, 0, 0]        

        self._add_function.connect("clicked", self._on_add_function)
        self._add_dicepool.connect("clicked", self._on_add_dicepool)

    def _on_add_function(self, button):

        display_content = self.display.get_text()

        name = self._drop_function.get_selected_item().get_string()
        parameters = self._parameters.get_text()

        content = display_content + f"{name} {parameters} in "

        self.display.set_text(content)
        

    def _on_add_dicepool(self, button):        

        display_content = self.display.get_text()

        amount = self._amount.get_text()
        faces = self._faces.get_text()
        adds = self._add_number.get_text()

        content = display_content + f"{amount}d{faces}{adds}"

        self.display.set_text(content)

        
    def _function_condition(self):
        print("nada")

