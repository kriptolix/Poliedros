# sidebar.py
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

from .logentry import LogEntry


@Gtk.Template(resource_path='/io/github/kriptolix'
              '/Poliedros/src/gtk/ui/EmptyPage.ui')
class EmptyPage(Adw.Bin):

    __gtype_name__ = 'EmptyPage'

    def __init__(self):

        super().__init__()


@Gtk.Template(resource_path='/io/github/kriptolix'
              '/Poliedros/src/gtk/ui/SideBar.ui')
class SideBar(Gtk.Box):

    __gtype_name__ = 'SideBar'

    _sidebar_list = Gtk.Template.Child()
    _clear_history_button = Gtk.Template.Child()

    def __init__(self):

        super().__init__()

        self._sidebar_list.set_selection_mode(Gtk.SelectionMode.NONE)

        self._sidebar_list.set_placeholder(EmptyPage())

        self._clear_history_button.connect(
            "clicked", lambda *_: self._sidebar_list.remove_all())

    def css_matching(self, splitview, param_spec):

        if splitview.get_collapsed():

            self._sidebar_list.remove_css_class("log_expanded")
            self._sidebar_list.add_css_class("log_collapsed")
            return

        self._sidebar_list.remove_css_class("log_collapsed")
        self._sidebar_list.add_css_class("log_expanded")

    def add_register(self, total, track, input):

        title = str(total)
        subtitle = track
        entry = LogEntry(title, subtitle, input)
        self._sidebar_list.insert(entry, 0)
