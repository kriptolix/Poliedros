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


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/UsageInfo.ui')
class UsageInfo(Adw.Dialog):
    __gtype_name__ = 'UsageInfo'

    _1 = Gtk.Template.Child()
    _2 = Gtk.Template.Child()
    _3 = Gtk.Template.Child()
    _4 = Gtk.Template.Child()
    _5 = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.connect("closed", lambda *_: self.close())

        rd_label = "Rolando dados - O comando para rolar dados utiliza operador 'd', \
        sendo formado pela quantidade de dados a ser rolada, o operador D, e o numero \
        de faces dos dados a serem rolados. \n \
        Ex.: 1d6, role um dado de seis faces \nEx.: 2d8, role dois dados de oito faces"

        self._2.set_text(rd_label)
        self._3.set_text(rd_label)
        self._4.set_text(rd_label)
        self._5.set_text(rd_label)
