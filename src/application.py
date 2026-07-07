# application.py
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


from gi.repository import Adw, Gio, GLib, Gtk, Gdk

import sys
from gettext import gettext as _

from .gtk.widgets.mainwindow import MainWindow
from .roller import execute_command
from .util import create_action
from .parser import parse_command


class PoliedrosApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.kriptolix.Poliedros',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        create_action(self, "app", 'quit',
                      lambda *_: self.quit(), ['<primary>q'])
        create_action(self, "app", 'about', self.on_about, None, None)
        create_action(self, "app", 'shortcuts', self.on_shortcuts, None, None)
        create_action(self, 'app', "roll", self.by_shortcut, ["<primary>r"])
        create_action(self, 'app', "toggle_mode",
                      self.by_shortcut, ["<primary>m"])
        create_action(self, 'app', "toggle_panel",
                      self.by_shortcut, ["<primary>p"])
        create_action(self, 'app', "clear_display",
                      self.by_shortcut, ["<primary>c"])
        create_action(self, 'app', "clear_registers",
                      self.by_shortcut, ["<primary>e"])
        create_action(self, 'app', "increment",
                      self.by_shortcut, ["<primary>equal", "<primary>KP_Add"])
        create_action(self, 'app', "decrement",
                      self.by_shortcut, ["<primary>minus", "<primary>KP_Subtract"])
        
        dice = {"df":0, "d4":1, "d6":2, "d8":3, "d10":4, "d12":5, "d20":6, "d100":7}

        for dice, key in dice.items():

            create_action(self, 'app', f"{dice}", self.by_shortcut,
                          [f"<primary>{key}", f"<primary>KP_{key}"])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self._window = self.props.active_window
        if not self._window:
            self._window = MainWindow(self)

        self._window.present()

        self._display = self._window._roll_area._display
        self._update_result = self._window._roll_area.update_result
        self._add_die = self._window._roll_area.add_die
        self._add_modifier = self._window._roll_area.add_modifier
        self._add_register = self._window._sidebar.add_register
        self._audio = self._window.selectors._audio
        self._render = self._window.selectors._render
        self._gl_area = self._window._roll_area._gl_area 


    def on_about(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog.new_from_appdata(
            '/io/github/kriptolix/Poliedros'
            '/data/io.github.kriptolix.Poliedros.metainfo.xml.in',
            '2.0.0'
        )

        about.set_translator_credits(_('translator_credits'))
        about.present(self.props.active_window)

    def on_shortcuts(self, *args):

        builder = Gtk.Builder.new_from_resource(
            '/io/github/kriptolix/Poliedros/src/gtk/ui/Shortcuts.ui'
        )

        shortcuts = builder.get_object("shortcuts")        
        shortcuts.present(self._window)

    def do_reroll(self, input):

        self._display.set_text(input)
        self.do_roll()

    def do_roll(self):

        input = self._display.get_text()

        try:
            node = parse_command(input)
        except ValueError as e:
            print(e)
            self._display.add_css_class("error")
            return        

        result = execute_command(node)
        total = result.get("result")
        log = result.get("log")
        target = result.get("rolls")

        audio = self._window.audio_enabled

        if self._window.render_enabled:

            spec = {}
            valid = True

            for key, values in target.items():
                spec[key] = len(values)

                if key not in ["df", "d4", "d6", "d8", "d10", "d12", "d20", "d100"]:                    
                    valid = False
                    break

            if valid:
                self._gl_area.start_simulation(audio, spec, target)       

        self._add_register(total, log, input)
        self._update_result(total)

    def by_shortcut(self, action: Gio.SimpleAction,
                    parameter: GLib.VariantType) -> None:

        name = action.get_name()

        match name:
            case 'roll':
                self.do_roll()
                return
            case "clear_display":
                self._window._roll_area.clear_display(None)
                return
            case "clear_registers":
                self._window._sidebar.clear_registers(None)
                return
            case "toggle_mode":
                state = self._window._roll_area._mode_button.get_active()

                if state:
                    self._window._roll_area._mode_button.set_active(False)
                else:
                    self._window._roll_area._mode_button.set_active(True)
                return
            case "toggle_panel":
                state = self._window._toggle_history_button.get_active()

                if state:
                    self._window._toggle_history_button.set_active(False)
                else:
                    self._window._toggle_history_button.set_active(True)
                return
            case "increment":                
                self._add_modifier(None, +1)
                return
            case "decrement":                
                self._add_modifier(None, -1)
                return

        
        self._add_die(name)    


def main(version):
    """The application's entry point."""
    app = PoliedrosApplication()
    return app.run(sys.argv)
