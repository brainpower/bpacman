
from gi.repository import Gtk
from bpacman.main_window import MainWindow

def main():
	win = MainWindow("bpacman 0.1.0");
	win.connect("delete-event", Gtk.main_quit);
	win.show_all();
	Gtk.main();
