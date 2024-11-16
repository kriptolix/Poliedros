# logentry.py
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
from gi.repository import GObject


@Gtk.Template(resource_path='/io/github/kriptolix'
              '/Poliedros/src/gtk/ui/LogEntry.ui')
class LogEntry(Adw.ActionRow):

    __gtype_name__ = 'LogEntry'

    input = GObject.Property(type=str, default=None)

    _reroll_button = Gtk.Template.Child()

    def __init__(self, title, subtitle, input):

        super().__init__()

        self.set_title(title)
        self.set_subtitle(subtitle)
        self.input = input

        self._reroll_button.connect("clicked", self._do_reroll)

    def _do_reroll(self, button):

        application = self.get_root().application
        application.do_reroll(self.input)
