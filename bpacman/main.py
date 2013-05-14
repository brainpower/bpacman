
from gi.repository import Gtk,Gdk,GLib
from bpacman.main_window import *

def main():
	print("bpacman 0.1.0 \"What a Pain\" using libalpm", pyalpm.alpmversion())
	win = MainWindow("bpacman 0.1.0");
	win.connect("delete-event", Gtk.main_quit);
	win.show_all();
	GLib.threads_init()
	Gdk.threads_init()
	Gdk.threads_enter()
	Gtk.main()
	Gdk.threads_leave()
