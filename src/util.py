# util.py
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

from gi.repository import Gio


def create_action(action_group, prefix, name, callback,
                  shortcuts=None, parameter=None, target=None):
    """
    Add an action to an action group.

    Args:
        action_group(Gio.SimpleActionGroup): where the actions is added
        prefix(str): prefix used to actions on action group
        name(str): the name of the action
        callback(function): the function to be called when the action is
            activated
        shortcuts(list): an optional list of accelerators
        parameter(GLib.VariantType): possibles parameters for the action
    """
    action = Gio.SimpleAction.new(name, parameter)
    action.connect("activate", callback)
    action_group.add_action(action)
    detailed_name = f"{prefix}.{name}"

    if (target):
        detailed_name = f"{prefix}.{name}::{target}"

    if shortcuts:
        action_group.set_accels_for_action(detailed_name, shortcuts)
