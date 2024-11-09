from gi.repository import Gtk, Adw, GObject


@Gtk.Template(resource_path='/io/gitlab/kriptolix'
              '/Poliedros/src/gtk/ui/LogEntry.ui')
class LogEntry(Adw.ActionRow):

    __gtype_name__ = 'LogEntry'

    input = GObject.Property(type=str, default=None)

    _reroll_button = Gtk.Template.Child()

    def __init__(self, title, subtitle, input):

        super().__init__()

        self.set_title(title)
        self.set_subtitle(subtitle)
        self.input = input

        self._reroll_button.connect("clicked", self._do_reroll)

    def _do_reroll(self, button):

        application = self.get_root().application
        application.do_reroll(self.input)
