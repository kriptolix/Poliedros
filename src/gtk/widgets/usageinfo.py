# usageinfo.py
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

from gettext import gettext as _


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/UsageInfo.ui')
class UsageInfo(Adw.Dialog):
    __gtype_name__ = 'UsageInfo'

    _rd_label = Gtk.Template.Child()
    _as_label = Gtk.Template.Child()
    _kh_label = Gtk.Template.Child()
    _kl_label = Gtk.Template.Child()
    _ed_label = Gtk.Template.Child()
    _cb_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.connect("closed", lambda *_: self.close())

        rd_text = _('<b>Rolling dice:</b> operator "d".\n\n<b>Ex.:</b> 1d6'
                    ', roll 1 6-sided die.\n<b>Ex.:</b> 2d8, roll 2 8-sided'
                    ' dice.')

        as_text = _('<b>Additions/Subtractions:</b> "+" and "-" operators.'
                    '\n\n<b>Ex.:</b> 1d6 + 3, roll 1 6-sided die and add '
                    'the number 3.\n<b>Ex.:</b> 2d8 - 1d4, roll 2 8-sided '
                    'dice and subtract the result of rolling 1 4-sided die.')

        kh_text = _('<b>Keeping higher:</b> operator "h".\n\n<b>Ex.:</b> '
                    '2h3d6, roll 3 6-sided dice and keep the 2 highest.'
                    '\n<b>Ex.:</b> 1h2d20 or h2d20, roll 2 20-sided dice '
                    'and keep the highest.')

        kl_text = _('<b>Keeping lower:</b> operator "l".\n\n<b>Ex.:</b> 2l4d10'
                    ', roll 4 10-sided dice and keep the 2 lowest.'
                    '\n<b>Ex.:</b> 1l3d6 or l3d6, roll 3 6-sided dice and '
                    'keep the lowest.')

        ed_text = _('<b>Exploding dice:</b> operator "e". \n\n<b>Ex.:</b> e6d6'
                    ', roll 6 6-sided dice and, if any of them result in a 6, '
                    'roll that die again, if the new result is also a 6, roll '
                    'that die again and so on indefinitely..\n<b>Ex.:</b> '
                    '1e5d10, roll 5 10-sided dice and, if any of them result '
                    'in a 10, roll that die again, if the new result is also'
                    ' a 10 the die will not be rolled again.')

        self._rd_label.set_markup(rd_text)
        self._as_label.set_markup(as_text)
        self._kh_label.set_markup(kh_text)
        self._kl_label.set_markup(kl_text)
        self._ed_label.set_markup(ed_text)
