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
from .gldicearea import GLDiceArea
#from .advancedmode import AdvancedMode

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
    _clamp = Gtk.Template.Child()
    _overlay = Gtk.Template.Child()
    # _advanced = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # df, d4, d6, d8, d10, d12, d20, d100
        self._command = {"df":0, "d4":0, "d6":0, "d8":0, "d10":0, "d12":0, "d20":0, "d100":0}
        
        self._modifier = 0
        # self._advanced.display = self._display

        self._roll_button.connect("clicked", self._do_roll)

        self._dice_area._d100_button.connect("clicked", self.add_die)
        self._dice_area._d20_button.connect("clicked", self.add_die)
        self._dice_area._d12_button.connect("clicked", self.add_die)
        self._dice_area._d10_button.connect("clicked", self.add_die)
        self._dice_area._d8_button.connect("clicked", self.add_die)
        self._dice_area._d6_button.connect("clicked", self.add_die)
        self._dice_area._d4_button.connect("clicked", self.add_die)
        self._dice_area._df_button.connect("clicked", self.add_die)

        self._dice_area._plus_button.connect("clicked", self.add_modifier, +1)
        self._dice_area._minus_button.connect("clicked", self.add_modifier, -1)

        self._clear_button.connect("clicked", self.clear_display)
        self._mode_button.connect("toggled", self.change_mode)

        buffer = self._display.get_buffer()

        buffer.connect("inserted-text", self._reset_error_state)
        buffer.connect("deleted-text", self._reset_error_state)

        self._display.connect("activate", self._do_roll)

        self._display.connect("changed",
                                 self._button_activation)
        
        self._button_activation(self._display)

        # self._overlay.set_child(GLDiceArea())

        # self._display.set_text("5d6 +1 |cn:>2")

    def _reset_error_state(self, *args):

        if self._display.has_css_class("error"):
            self._display.remove_css_class("error")

    def update_result(self, total):

        self._results.set_text(str(total))

    def clear_display(self, button):
        self._command = {"df":0, "d4":0, "d6":0, "d8":0, "d10":0, "d12":0, "d20":0, "d100":0}
        self._modifier = 0
        self._display.set_text("")
        self._results.set_text("?")

    def change_mode(self, button):

        placeholder = "Ex.: 2d6, 1d12+3, 2d20|kh:1"

        if self._mode_button.get_active():
            self._stack.set_visible_child(self._info_area)
            self._display.set_editable(True)
            self._display.set_can_focus(True)
            self._display.set_placeholder_text(placeholder)
            self._display.grab_focus()
            return
       
        self._stack.set_visible_child(self._dice_area)
        self._display.set_editable(False)
        self._display.set_can_focus(False)
        self._display.set_placeholder_text('')
        self.clear_display(None)

    def _assemble_command(self):
        
        display_content = ""
        content = ""

        parts = []

        for dice, quantity in self._command.items():
            if quantity > 0:
                parts.append(f"{quantity}{dice}")         
        
        if self._modifier > 0:
            content = (f" + {self._modifier}")
       
        if self._modifier < 0:
            content =(f" - {abs(self._modifier)}")

        display_content = " + ".join(parts)
        display_content = display_content + content
        
        self._display.set_text(display_content)

    def add_die(self, button):

        die_key = button

        if not isinstance(button, str):
            die_key = button.get_tooltip_text()        

        self._command[die_key] += 1
        self._assemble_command()

    def add_modifier(self, button, modifier):
        self._modifier += modifier
        self._assemble_command()

    def _do_roll(self, button):

        application = self.get_root().application
        application.do_roll()
        self._command = {"df":0, "d4":0, "d6":0, "d8":0, "d10":0, "d12":0, "d20":0, "d100":0}

    def _button_activation(self, display):
        
        has_text = bool(display.get_text().strip())
        self._roll_button.set_sensitive(has_text)