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
from gi.repository import Gtk

from gettext import gettext as _


@Gtk.Template(resource_path='/io/gitlab/kriptolix/'
              'Reinput/src/gtk/ui/dialogs.ui')
class Dialogs(Adw.MessageDialog):
    __gtype_name__ = 'Dialogs'

    def __init__(self, window):
        super().__init__()

        self.set_transient_for(window)
        self.body = ""
        self.heading = ""
        # self.data = data

        match type:
            case "add_group":
                self._create_group()
            case "add_input":
                self._save_project()
            case "add_output":
                self._recovery_unsaved()
            case "remove_group":
                self._remove_section()
            case "remove_input":
                self._remove_note()
            case "remove_output":
                self._remove_note()

        self.set_body(self.body)
        self.set_heading(self.heading)
        self.present()

    def _remove_section(self):

        self.add_response("cancel",  _("_Cancel"))
        self.add_response("delete",    _("_Delete"))

        self.set_response_appearance("delete", 2)

        self.heading = _("Delete section?")
        self.body = _("Delete this section will remove "
                      "all sub sections of this section and "
                      "the text attached to them")
        
    def _create_group(self):

        def enter_key_pressed(widget):

            self.response("create")
            self.close()

        def avoid_empty_name(buffer, length):

            if (buffer.get_length() > 0):
                self.set_response_enabled("create", True)
            else:
                self.set_response_enabled("create", False)

        ##
        self._entry = Gtk.Entry.new()

        self.set_extra_child(self._entry)

        self.buffer = self._entry.get_buffer()

        self.add_response("cancel",  _("_Cancel"))
        self.add_response("create",    _("_Create"))
        self.set_response_appearance("create", 1)
        self.set_default_response("cancel")
        self.set_response_enabled("create", False)

        self.heading = _("Project Title")        

        self._entry.set_input_hints(Gtk.InputHints.NONE)
        self._entry.set_input_purpose(Gtk.InputPurpose.FREE_FORM)

        self._entry.connect("activate", enter_key_pressed)
        self.buffer.connect("notify::length", avoid_empty_name)

