from gi.repository import Gtk


@Gtk.Template(resource_path='/io/gitlab/kriptolix'
              '/Poliedros/src/gtk/ui/Menu.ui')
class Menu(Gtk.PopoverMenu):

    __gtype_name__ = 'Menu'

    def __init__(self):

        super().__init__()



