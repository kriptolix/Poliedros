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


@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/UsageInfo.ui')
class UsageInfo(Adw.Dialog):
    __gtype_name__ = 'UsageInfo'

    _textview = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.connect("closed", lambda *_: self.close())

    def resize_dialog(self, window):

        width = window.get_width() * 0.9
        height = window.get_height() * 0.9
        self.set_content_width(width)
        self.set_content_height(height)

        text = ("<b>Ex.:</b> value:<>15: greater than number(inclusive)."
                "<b>Ex.:</b> 6,8,10; relation of arbiterary numbers."
                "<b>Ex.:</b> 4; a singles number."
                "<b>Ex.:</b> 10: lower than number (inclusive)."
                "<b>Ex.:</b> 80..90; Interval between numbers (inclusive)."
                "from markup due to error parsing markup: Error on line 3 char"
                "21: “>” is not a valid character following a “<” character; "
                "it may not begin an element name"
                )

        buffer = self._textview.get_buffer()
        buffer.set_text(text)
