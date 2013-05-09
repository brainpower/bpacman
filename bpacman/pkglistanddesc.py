
from gi.repository import Gtk, Pango
from bpacman.pacman import Pacman

class PkgListAndDesc(Gtk.Paned):

	def __init__(self, model, *args, **kwargs):
		Gtk.Paned.__init__(self, *args, **kwargs);

		self.tbuff = Gtk.TextBuffer();
		self.create_default_tags();

		begin = self.tbuff.get_start_iter()

		self.tbuff.insert_with_tags_by_name(begin, "Description\n", "h1");
		self.tbuff.insert(begin, "\nSome blah, blah...\n")
		self.tbuff.insert(begin, "Some blah, blah...")

		sw1 = Gtk.ScrolledWindow(vexpand=True)
		sw2 = Gtk.ScrolledWindow(vexpand=True)

		treeview = Gtk.TreeView(model);
		descr = Gtk.TextView(buffer=self.tbuff, editable=False, cursor_visible=False, left_margin=8, right_margin=8);

		sw1.add(treeview);
		sw2.add(descr);
		self.add(sw1);
		self.add(sw2);

	def create_default_tags(self):
		self.tbuff.create_tag( "h1", size_points=16, weight=Pango.Weight.BOLD, pixels_above_lines=8)
