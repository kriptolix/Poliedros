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

    def css_matching(self, splitview, param_spec):

        if splitview.get_collapsed():

            self._sidebar_list.remove_css_class("log_expanded")
            self._sidebar_list.add_css_class("log_collapsed")
            return

        self._sidebar_list.remove_css_class("log_collapsed")
        self._sidebar_list.add_css_class("log_expanded")

    def add_register(self, total, track, input):

        title = str(total)
        subtitle = track
        entry = LogEntry(title, subtitle, input)
        self._sidebar_list.insert(entry, 0)
