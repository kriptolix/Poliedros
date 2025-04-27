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
from .numberpopover import NumberPopover

@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/AdvancedMode.ui')
class AdvancedMode(Gtk.Box):
    __gtype_name__ = 'AdvancedMode'

    #_results = Gtk.Template.Child()
    

    def __init__(self):
        super().__init__()
