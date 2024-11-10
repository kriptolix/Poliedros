# main.py
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


from .roller import execute_command
from .util import create_action

from .gtk.widgets.mainwindow import MainWindow

from gi.repository import Gio
from gi.repository import Adw

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')


class PoliedrosApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.gitlab.kriptolix.Poliedros',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        create_action(self, "app", 'quit',
                      lambda *_: self.quit(), ['<primary>q'])
        create_action(self, "app", 'about', self.on_about, None, None)

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
        self._add_register = self._window._sidebar.add_register

    def on_about(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='Poliedros',
                                application_icon='io.gitlab.kriptolix.Poliedros',
                                developer_name='k',
                                version='1.0',
                                developers=['k'],
                                copyright='© 2024 k')

        about.set_translator_credits(('k'))
        about.present(self.props.active_window)

    def do_reroll(self, input):

        self._display.set_text(input)
        self.do_roll()

    def do_roll(self):

        input = self._display.get_text()

        result, total, track = execute_command(input)

        if not result:
            print(total, track)
            self._display.add_css_class("error")
            return

        self._add_register(total, track, input)
        self._update_result(total)


def main(version):
    """The application's entry point."""
    app = PoliedrosApplication()
    return app.run(sys.argv)
