# LinuxUtils
Tiny and Useful tools

##English to Chinese translate
file:`dict.py`

Translate selected word by http://dict.cn.

##Search word
file:`googleWord.py`

Search the selected word by https://www.google.com.hk.

#Install:

sudo pacman -S libnotify python-gobject mplayer python-pip
sudo python -m pip install beautifulsoup4

Those tiny tools depends on the 'xsel' command
~~~~{bash}
	apt-get install xsel
~~~~

##Map to them to you favorite shortcut:
Example:
* shortcut:	F2
* command:	python /path/to/repo/dict.py


