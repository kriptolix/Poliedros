--disable-rofiles-fuse

* replace Gtk.ShortcutsWindow with Adw.ShortcutsDialog
* normalize the way roll is created to integrate 3d dice roll

roadmap fo splitted resolution mechanics:

Advanced mode on:
* render off
* audio off
* no 3d simulation

like actual away, get texto from display sendo to roller execute_command

Advanced mode off and render mode off:

* audio off
* no 3d simulation

like actual away, get texto from display and sendo to roller execute_command

Advanced mode off and render mode on:

* audio on or off

- get command directly from rollarea
- sendo to simulation 
- get results an apply to log

create a way to format the Results response and sum increment outside of roller.