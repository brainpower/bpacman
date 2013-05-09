
from gi.repository import Gtk
from bpacman.sidebar import Sidebar
from bpacman.pkglistanddesc import PkgListAndDesc

class PkgView(Gtk.Paned):

	def __init__(self, *args):
		Gtk.Paned.__init__(self, *args);

		self.set_orientation(Gtk.Orientation.HORIZONTAL);
		self.set_vexpand(True)

		tlst = Gtk.ListStore(str)
		sidebar = Sidebar();
		pkglist = PkgListAndDesc(tlst, orientation=Gtk.Orientation.VERTICAL);

		self.add(sidebar);
		self.add(pkglist);
