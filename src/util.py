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
        data(GLib.VariantType): possibles parameters for the action
    """
    action = Gio.SimpleAction.new(name, parameter)
    action.connect("activate", callback)
    action_group.add_action(action)
    detailed_name = f"{prefix}.{name}"

    if (target):
        detailed_name = f"{prefix}.{name}::{target}"

    if shortcuts:
        action_group.set_accels_for_action(detailed_name, shortcuts)
