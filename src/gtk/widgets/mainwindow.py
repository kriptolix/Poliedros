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
from gi.repository import Gtk, Gdk

from .rollarea import RollArea

@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Poliedros/src/gtk/ui/MainWindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/io/gitlab/kriptolix/'
                                        'Poliedros/data/poliedros.css')
        add_provider = Gtk.StyleContext.add_provider_for_display
        add_provider(Gdk.Display.get_default(),
                     css_provider,
                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
