# mainwindow.py
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
from gi.repository import Gdk
from gi.repository import GObject

from .rollarea import RollArea
from .sidebar import SideBar


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/MainWindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    _about_button = Gtk.Template.Child()
    _split_view = Gtk.Template.Child()
    _toggle_history_button = Gtk.Template.Child()
    _back_button = Gtk.Template.Child()
    _sidebar = Gtk.Template.Child()
    _roll_area = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app)

        self.application = app

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/io/gitlab/kriptolix/'
                                        'Poliedros/data/poliedros.css')
        add_provider = Gtk.StyleContext.add_provider_for_display
        add_provider(Gdk.Display.get_default(),
                     css_provider,
                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self._split_view.bind_property("show-sidebar", self._toggle_history_button, "active",
                                       GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        self._split_view.bind_property("collapsed", self._back_button, "visible",
                                       GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        self._back_button.connect(
            "clicked", lambda *_: self._split_view.set_show_sidebar(False))

        self._about_button.set_action_name("app.about")

        self._split_view.connect("notify::collapsed",
                                 self._sidebar.css_matching)
