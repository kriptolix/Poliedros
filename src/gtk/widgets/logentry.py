from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/io/gitlab/kriptolix'
              '/Poliedros/src/gtk/ui/LogEntry.ui')
class LogEntry(Adw.ActionRow):

    __gtype_name__ = 'LogEntry'

    def __init__(self, title, subtitle):

        super().__init__()

        self.set_title(title)
        self.set_subtitle(subtitle)

    def _redo_roll(self):

        self.get_subtitle()