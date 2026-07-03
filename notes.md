--disable-rofiles-fuse

xgettext \
  --files-from=po/POTFILES.in \
  --from-code=UTF-8 \
  --keyword=_ \
  --output=po/seuapp.pot

* replace Gtk.ShortcutsWindow with Adw.ShortcutsDialog [ok]
* normalize the way roll is created to integrate 3d dice roll [ok]
* clear render area with clear button [ok]
* update translations [ok]
* insert date on metadata file
* merge modules on manifest
