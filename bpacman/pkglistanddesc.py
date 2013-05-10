import sys
from gi.repository import Gtk, Pango
from bpacman.pacman import Pacman

class PkgListAndDesc(Gtk.Paned):

	def __init__(self, *args, **kwargs):
		Gtk.Paned.__init__(self, *args, **kwargs);

		self._tbuff = Gtk.TextBuffer();
		self._create_default_tags();
		self._update_description("bpacman", "A graphical frontend to pacman, the Arch Linux package manager, inspired by the synaptic package manager.")

		sw1 = Gtk.ScrolledWindow(hexpand=True, shadow_type=Gtk.ShadowType.IN)
		sw2 = Gtk.ScrolledWindow(hexpand=True, shadow_type=Gtk.ShadowType.IN)

		self._models = {}
		self._sort_type = Gtk.SortType.ASCENDING;

		self._tv = Gtk.TreeView();
		self._tv.set_headers_clickable(True)
		self._create_columns();
		descr = Gtk.TextView(buffer=self._tbuff, editable=False, cursor_visible=False, left_margin=8, right_margin=8);
		descr.set_wrap_mode(Gtk.WrapMode.WORD)

		self._tv.get_selection().connect("changed", self._tv_selection_changed)

		sw1.add(self._tv);
		sw2.add(descr);
		sw1.set_property("height-request", 130)

		self.pack1(sw1, resize=True);
		self.pack2(sw2);

	def _create_default_tags(self):
		self._tbuff.create_tag( "h1", size_points=16, weight=Pango.Weight.BOLD, pixels_above_lines=8)
		self._tbuff.create_tag( "b", weight=Pango.Weight.BOLD)

	def _create_columns(self):
		state = Gtk.TreeViewColumn(None, Gtk.CellRendererPixbuf(), pixbuf=1)
		name  = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=2)
		iver  = Gtk.TreeViewColumn("Installed Version", Gtk.CellRendererText(), text=3)
		lver  = Gtk.TreeViewColumn("Latest Version", Gtk.CellRendererText(), text=4)
		desc  = Gtk.TreeViewColumn("Description", Gtk.CellRendererText(), text=5)
		state.set_resizable(True)
		name.set_resizable(True)
		iver.set_resizable(True)
		lver.set_resizable(True)
		desc.set_resizable(True)
		name.set_clickable(True)
		name.set_sort_indicator(True)
		name.connect("clicked", self._swap_sort_order)
		self._name_column = name
		self._tv.append_column(state)
		self._tv.append_column(name)
		self._tv.append_column(iver)
		self._tv.append_column(lver)
		self._tv.append_column(desc)

	def _swap_sort_order(self, b):
		print("swap")
		if self._sort_type == Gtk.SortType.ASCENDING:
			self._sort_type = Gtk.SortType.DESCENDING
		else:
			self._sort_type = Gtk.SortType.ASCENDING;
		self._tv.get_model().set_sort_column_id(2, self._sort_type)
		b.set_sort_order(self._sort_type)
		b.set_sort_indicator(True)

	def _tv_selection_changed(self, selection):
		pacman = Pacman.Instance();
		if not selection:
			return
		model,it = selection.get_selected()
		if it:
			repo = model[it][0]
			pkgn = model[it][2]
			pkg = pacman.get_package(repo, pkgn);
			self._update_description(pkgn, pkg.desc)

	def _update_description(self, pkgname, desc):
		self._tbuff.set_text("")
		begin = self._tbuff.get_start_iter()

		self._tbuff.insert_with_tags_by_name(begin, pkgname+"\n", "h1");
		self._tbuff.insert(begin, "\n")
		self._tbuff.insert(begin, desc)

	#~ def _update_models(self):
		#~ pacman = Pacman.Instance();
#~
		#~ self._models["All"] = Gtk.ListStore(str)
		#~ for repo in pacman.get_repos():
			#~ for pkg in pacman.get_package_list(repo):
				#~ self._models["All"].append([pkg.name])

	def add_pkg_model(self, name, model):
		self._models[name] = model;

	def set_package_model(self, model):
		try:
			self._tv.set_model(self._models[model])
		except KeyError:
			sys.stderr.write("[PkgListAndDesc] Warning: Model for '%s' not registered.\n" % model)
		self._name_column.set_sort_indicator(True)
		self._name_column.set_sort_order(self._sort_type)
