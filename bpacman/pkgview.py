
from gi.repository import Gtk
from bpacman.sidebar import Sidebar
from bpacman.pkglistanddesc import PkgListAndDesc

class PkgView(Gtk.Paned):

	def __init__(self, *args):
		Gtk.Paned.__init__(self, margin=4, *args);

		self.set_orientation(Gtk.Orientation.HORIZONTAL);
		self.set_vexpand(True)

		pkglist = PkgListAndDesc(orientation=Gtk.Orientation.VERTICAL);
		sidebar = Sidebar(pkglist);

		sidebar.set_property("width-request", 180)

		self.add(sidebar);
		self.add(pkglist);
