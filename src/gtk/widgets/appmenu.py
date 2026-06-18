from gi.repository import Gtk

@Gtk.Template(resource_path='/io/github/kriptolix'
              '/Poliedros/src/gtk/ui/Selectors.ui')
class Selectors(Gtk.Box):

    __gtype_name__ = 'Selectors'


    _audio = Gtk.Template.Child()
    _render = Gtk.Template.Child()

    def __init__(self):

        super().__init__()


@Gtk.Template(resource_path='/io/github/kriptolix'
              '/Poliedros/src/gtk/ui/AppMenu.ui')
class AppMenu(Gtk.PopoverMenu):

    __gtype_name__ = 'AppMenu'

    def __init__(self):

        super().__init__()

        self._selectors = Selectors()
        self.add_child(self._selectors, "selectors")