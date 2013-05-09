
from gi.repository import Gtk
from bpacman.pacman import Pacman

class Sidebar(Gtk.Grid):

	def __init__(self, *args, **kwargs):
		Gtk.Grid.__init__(self, *args, orientation=Gtk.Orientation.VERTICAL, row_spacing=5, **kwargs);

		self._group_lst = Gtk.ListStore(str);
		self._state_lst = Gtk.ListStore(str);
		self._repos_lst = Gtk.ListStore(str);
		self._filters_lst = Gtk.ListStore(str);
		self._searches_lst = Gtk.ListStore(str);
		self._arch_lst = Gtk.ListStore(str);

		self._update_lists();

		sw = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
		self._treeview = Gtk.TreeView(self._group_lst);
		self._treeview.set_vexpand(True)
		self._treeview.set_headers_visible(False)
		self._treeview.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))

		button_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL);
		self._add_buttons(button_grid)

		sw.add(self._treeview);
		self.add(sw);
		self.add(button_grid);

	def _update_lists(self):
		pacman = Pacman.Instance();
		for repo in pacman.get_repos():
			self._repos_lst.append([repo])

		for g in pacman.get_groups():
			self._group_lst.append([g])

	def _on_g_button(self, b):
		self._treeview.set_model(self._group_lst)

	def _on_s_button(self, b):
		self._treeview.set_model(self._state_lst)

	def _on_r_button(self, b):
		self._treeview.set_model(self._repos_lst)

	def _on_f_button(self, b):
		self._treeview.set_model(self._filters_lst)

	def _on_sr_button(self, b):
		self._treeview.set_model(self._searches_lst)

	def _on_a_button(self, b):
		self._treeview.set_model(self._arch_lst)

	def _add_buttons(self, button_grid):
		g_button = Gtk.Button("Groups", hexpand=True)
		s_button = Gtk.Button("Status", hexpand=True)
		r_button = Gtk.Button("Repos", hexpand=True)
		f_button = Gtk.Button("Filters", hexpand=True)
		sr_button= Gtk.Button("Search Results", hexpand=True)
		a_button = Gtk.Button("Architecture", hexpand=True)
		g_button.connect("clicked", self._on_g_button)
		s_button.connect("clicked", self._on_s_button)
		r_button.connect("clicked", self._on_r_button)
		f_button.connect("clicked", self._on_f_button)
		sr_button.connect("clicked", self._on_sr_button)
		a_button.connect("clicked", self._on_a_button)
		button_grid.add(g_button)
		button_grid.add(s_button)
		button_grid.add(r_button)
		button_grid.add(f_button)
		button_grid.add(sr_button)
		button_grid.add(a_button)
