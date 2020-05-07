#!/usr/bin/python
#coding:utf8
#Dependencies: libnotify, python-gobject (or python2-gobject for Python 2) mplayer
# pip install beautifulsoup4

import gi
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from gi.repository import Notify
from gi.repository import Gtk, Gdk, GObject
import requests
import json
from bs4 import BeautifulSoup as bs

def getFromDialog():
    txt=""
    class EntryWindow(Gtk.Window):

        def keyPress(self, widget, event):
            if Gdk.keyval_name(event.keyval) == 'Return':
                nonlocal txt
                txt= self.entry.get_text()
                lookupAndShow(txt)
                if not self.pined:
                    Gtk.main_quit()
                return True
            return False
        def __init__(self):
            Gtk.Window.__init__(self, title="Entry word")
            self.set_size_request(200, 100)

            self.timeout_id = None
            self.pined = False

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.add(vbox)

            self.entry = Gtk.Entry()
            self.entry.set_text("")

            self.entry.connect('key-press-event', self.keyPress)
            vbox.pack_start(self.entry, True, True, 0)

            hbox = Gtk.Box(spacing=0)
            vbox.pack_start(hbox, True, True, 0)
            
            self.check_visible = Gtk.CheckButton("Pin it :>")
            self.check_visible.connect("toggled", self.on_visible_toggled)
            self.check_visible.set_active(False)
            hbox.pack_start(self.check_visible, True, True, 0)

            self.on_editable_toggled()
            self.on_pulse_toggled()
            self.on_icon_toggled()

        def on_editable_toggled(self):
            self.entry.set_editable(True)

        def on_visible_toggled(self, button):
            value = button.get_active()
            self.pined = value

        def on_pulse_toggled(self):
            self.entry.set_progress_pulse_step(0.2)
            # Call self.do_pulse every 100 ms
            self.timeout_id = GObject.timeout_add(100, self.do_pulse, None)

        def do_pulse(self, user_data):
            self.entry.progress_pulse()
            return True

        def on_icon_toggled(self):
            icon_name = "system-search-symbolic"
            self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
                icon_name)

    win = EntryWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    return txt

def getSelectedTxt():
    cb = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    txt = cb.wait_for_text()
    print("txt:"+str(txt)+"len:"+str(len(txt)))
    if len(txt) > 30:
        print("max lenth current is 15, wipe data")
        txt = ""
    if len(txt) <= 2:
        print("min lenth current is 2, wipe data")
        txt = ""

    txt = txt.strip(":;,.()!~-+{}[]?/“”\n")
    txt = txt.replace("-\n", "")
    if len(txt) == 0:
        txt = getFromDialog()
    else:
        lookupAndShow(txt)

    return txt
def showNotify(title, txt):
    Notify.init("dict")
    Hello=Notify.Notification.new(title, txt, "dialog-information")
    Hello.set_urgency(2)
    Hello.show()

def complete(word):
    words = json.loads(requests.ger('http://dict.cn/apis/suggestion.php?q='+word).content)

def lookup(word):
    soup = bs(requests.get('http://dict.cn/'+word, "html.parser").content.decode('utf8')).find('div', {'class':'main'})
    if soup.find('div', {'class':'ifufind'}) != None:
        print('not found')
        return
    root = soup.find('h1', {'class':'keyword'}).text
    phonetic = soup.find('div', {'class':'phonetic'}).findAll('span')[1]
    sound = ['http://audio.dict.cn/'+i['naudio'].split('?')[0]+'t='+root for i in phonetic.findAll('i')]
    try:
        pronunciation = phonetic.find('bdo').text
    except:
        pronunciation = ""
    definition = [i.text for i in soup.find('div', {'class':'basic clearfix'}).find('ul').findAll('li')[:-1]]
    #print paint(root, 'bright green'), paint(pronunciation, 'bright yellow')
    contentNow = u""

    for i in definition: 
        contentNow += i.replace('\n', '').replace('\t','') +"\n"


    showNotify(word + u" " + pronunciation, contentNow)
    return [root, sound]


import subprocess
def play(url):
    for i in url:
        print(i)
        subprocess.check_output(['mplayer', '-really-quiet', i], stderr=subprocess.STDOUT)

def lookupAndShow(txt):
    if len(txt) == 0:
        showNotify("Opps", "输入为空")
        return
    
    r = lookup(txt)
    if r == None:
        showNotify(u"Oppus..", u"Not Found")
        return
    t = Thread(target=play, args=(r[1],))
    t.daemon=True
    t.start()
    #star(r[0]) #uncomment this line to star the word while lookup
    t.join()

from sys import argv
from threading import Thread
def main():
    txt = getSelectedTxt()
if __name__ == '__main__':
    main()
