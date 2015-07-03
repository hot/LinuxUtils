#!/usr/bin/python
import webbrowser
from subprocess import check_output
txt = check_output(["xsel"])

if len(txt) > 0:
    webbrowser.open_new_tab("http://dict.cn/" + txt)

