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


@Gtk.Template(resource_path='/io/github/kriptolix/'
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
        css_provider.load_from_resource('/io/github/kriptolix/'
                                        'Poliedros/data/poliedros.css')
        add_provider = Gtk.StyleContext.add_provider_for_display
        add_provider(Gdk.Display.get_default(),
                     css_provider,
                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # self.style_manager = Adw.StyleManager.get_default()

        flags = GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL
        self._split_view.bind_property("show-sidebar",
                                       self._toggle_history_button,
                                       "active", flags)

        self._split_view.bind_property("collapsed",
                                       self._back_button,
                                       "visible", flags)

        self._back_button.connect(
            "clicked", lambda *_: self._split_view.set_show_sidebar(False))

        self._about_button.set_action_name("app.about")

        self._split_view.connect("notify::collapsed",
                                 self._sidebar.css_matching)

        width_condition = Adw.BreakpointCondition.parse("max-width: 535sp")
        
        width_breakpoint = Adw.Breakpoint.new(width_condition)
        width_breakpoint.connect("apply", self._breakpoint_apply, 0)
        width_breakpoint.connect("unapply", self._breakpoint_unapply, 0)

        self.add_breakpoint(width_breakpoint)        

        ratio_condition = Adw.BreakpointCondition.parse(
            "min-aspect-ratio: 3/2 and max-width: 725sp")
        ratio_breakpoint = Adw.Breakpoint.new(ratio_condition)
        ratio_breakpoint.connect("apply", self._breakpoint_apply, 1)
        ratio_breakpoint.connect("unapply", self._breakpoint_unapply, 1)

        self.add_breakpoint(ratio_breakpoint)

        

    def _breakpoint_apply(self, breakpoint, data):

        if data == 0:
            self._split_view.set_collapsed(True)
            return

        # self._roll_area._dice_area.set_orientation(0)
        self._roll_area._adaptable.set_orientation(0)
        self._roll_area._results.set_halign(1)
        self._roll_area._stack.set_halign(2)
        self._roll_area._dice_area.set_halign(2)
        self._roll_area._adaptable.set_spacing(5)

    def _breakpoint_unapply(self, breakpoint, data):

        if data == 0:
            self._split_view.set_collapsed(False)
            return       

        # self._roll_area._dice_area.set_orientation(1)
        self._roll_area._adaptable.set_orientation(1)
        self._roll_area._results.set_halign(3)
        self._roll_area._stack.set_halign(3)
        self._roll_area._dice_area.set_halign(3)
        self._roll_area._adaptable.set_spacing(20)