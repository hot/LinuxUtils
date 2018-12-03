#!/usr/bin/python
import webbrowser
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from gi.repository import Gtk, Gdk
from subprocess import check_output

def getSelectedTxt():
    cb = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    txt = cb.wait_for_text()
    return txt
txt = getSelectedTxt()

if len(txt) > 0:
    '+'.join(txt.split(' '))
    webbrowser.open_new_tab("https://www.google.com.hk/search?q=" + txt)

