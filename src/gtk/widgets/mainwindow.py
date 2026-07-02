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
from .appmenu import AppMenu


@Gtk.Template(resource_path='/io/github/kriptolix/'
              'Poliedros/src/gtk/ui/MainWindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    _menu_button = Gtk.Template.Child()   
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

        self.style_manager = Adw.StyleManager.get_default()        
        
        self.style_manager.connect("notify::dark", self.on_theme_changed)
        

        flags = GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL
        self._split_view.bind_property("show-sidebar",
                                       self._toggle_history_button,
                                       "active", flags)

        self._split_view.bind_property("collapsed",
                                       self._back_button,
                                       "visible", flags)

        self._back_button.connect(
            "clicked", lambda *_: self._split_view.set_show_sidebar(False))        

        self._split_view.connect("notify::collapsed",
                                 self._sidebar.css_matching)
        
        self._sidebar.css_matching(self._split_view, None)

        width_condition = Adw.BreakpointCondition.parse("max-width: 520sp")

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
        
        popover = AppMenu()        
        popover.set_offset(-30, 0)             
        self._menu_button.props.popover = popover

        self.selectors = popover.selectors
        
        self._breakpoints_active = [False, False]

        self._roll_area._gl_area.theme = self.theme

        self.selectors._render.connect("notify::active", self.on_render_changed)
                

    def _breakpoint_apply(self, breakpoint, data):

        self._breakpoints_active[data] = True

        if data == 0:
            self._split_view.set_collapsed(True)
            self._roll_area._mode_button.set_visible(False)
            return
          
        self._roll_area._mode_button.set_visible(False)
        self._split_view.set_collapsed(True)
        self._roll_area.set_orientation(0)
        self._roll_area._clamp.set_halign(2)
        self._roll_area._clamp.set_margin_end(5)        
        

    def _breakpoint_unapply(self, breakpoint, data):

        self._breakpoints_active[data] = False

        if data == 0:
            self._split_view.set_collapsed(False)
            self._roll_area._mode_button.set_visible(True)
            return
        
        if not any(self._breakpoints_active):

            self._roll_area.set_orientation(1)
            self._roll_area._clamp.set_halign(3)
            self._roll_area._clamp.set_margin_end(0)
            self._roll_area._mode_button.set_visible(True) 

    def on_theme_changed(self, param, value):                
        self._sidebar.css_matching(self._split_view, None)
        self._roll_area._gl_area.theme = self.theme

    def on_render_changed(self, button, value):
        
        if self.render_enabled:
             self.selectors._audio.set_sensitive(True)
             return
        
        self.selectors._audio.set_sensitive(False)
        self._roll_area._gl_area._sim.reset()

    @property
    def audio_enabled(self) -> bool:
        return self.selectors._audio.get_active()

    @property
    def render_enabled(self) -> bool:
        return self.selectors._render.get_active()

    @property
    def theme(self) -> str:
        if self.style_manager.get_dark():
            return "dark"
        return "light"  



        
        

        