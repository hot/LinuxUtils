#!/usr/bin/python
import webbrowser
from subprocess import check_output
txt = check_output(["xsel"])

if len(txt) > 0:
    '+'.join(txt.split(' '))
    webbrowser.open_new_tab("https://www.google.com.hk/search?q=" + txt)

