from gi.repository import Gtk, Adw

from .logentry import LogEntry


@Gtk.Template(resource_path='/io/gitlab/kriptolix'
              '/Poliedros/src/gtk/ui/EmptyPage.ui')
class EmptyPage(Adw.Bin):

    __gtype_name__ = 'EmptyPage'

    def __init__(self):

        super().__init__()


@Gtk.Template(resource_path='/io/gitlab/kriptolix'
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

    def add_register(self, results, command):

        title = str(results[0])
        subtitle = results[1]
        entry = LogEntry(title, subtitle, command)
        self._sidebar_list.insert(entry, 0)
