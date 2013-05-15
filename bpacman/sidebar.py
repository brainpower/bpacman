from gi.repository import Gtk,GdkPixbuf

from bpacman import utils
from bpacman.pacman import *

class Sidebar(Gtk.Grid):

	def __init__(self, pkgview, *args, **kwargs):
		Gtk.Grid.__init__(self, *args, orientation=Gtk.Orientation.VERTICAL, row_spacing=5, **kwargs);
		self._pkgview = pkgview

		self._group_lst = Gtk.ListStore(str);
		self._state_lst = Gtk.ListStore(str);
		self._repos_lst = Gtk.ListStore(str);
		self._filters_lst = Gtk.ListStore(str);
		self._searches_lst = Gtk.ListStore(str);

		self._group_lst.set_sort_column_id(0, Gtk.SortType.ASCENDING)
		self._filters_lst.set_sort_column_id(0, Gtk.SortType.ASCENDING)


		self._update_lists();
		self._treeview = Gtk.TreeView(self._group_lst);
		self._update_models();

		sw = Gtk.ScrolledWindow(vexpand=True, hexpand=True, shadow_type=Gtk.ShadowType.IN)

		self._treeview.set_vexpand(True)
		self._treeview.set_hexpand(True)
		self._treeview.set_headers_visible(False)
		self._treeview.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))

		self._treeview.get_selection().connect("changed", self._tv_selection_changed)
		self._treeview.get_selection().select_path(0)

		self._button_grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL, row_spacing=2, hexpand=True);
		self._add_buttons(self._button_grid)

		sw.add(self._treeview);
		self.add(sw);
		self.add(self._button_grid);

	def _update_lists(self):
		pacman = Pacman.Instance();

		self._group_lst.append(["All"])
		self._state_lst.append(["All"])
		self._repos_lst.append(["All"])

		groups = pacman.get_groups()
		for repo in pacman.get_repos():
			self._repos_lst.append([repo])

			for g in groups[repo]:
				if not utils.is_in(self._group_lst, g, lambda x, y: x[0] == y):
					self._group_lst.append([g])

		for state in ("Installed", "Installed (as dependency)", "Installed (manual)", "Installed (local)", "Not Installed", "Upgradeable"):
			self._state_lst.append([state])

	def _update_models(self):
		self._update_model_all_and_grps()
		self._update_state_models()

	def _update_state_models(self):
		self._update_model_installed()
		self._update_model_installed_dep()
		self._update_model_installed_man()
		self._update_model_installed_loc()
		self._update_model_not_installed()
		self._update_model_upgradeable()
		self._update_selected_model()

	def _update_model_installed(self):
		pacman = Pacman.Instance();
		minst = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_installed_pkgs():
			for r in pacman.get_repos():
				spkg = pacman.get_package(r,pkg.name)
				if spkg:
					break
			minst.append(self._pkgview._pkg_to_model(spkg, pkg))
		self._pkgview.add_pkg_model("Installed", minst);

	def _update_model_installed_dep(self):
		pacman = Pacman.Instance();
		minst = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_installed_pkgs(True):
			for r in pacman.get_repos():
				spkg = pacman.get_package(r,pkg.name)
				if spkg:
					break
			minst.append(self._pkgview._pkg_to_model(spkg, pkg))
		self._pkgview.add_pkg_model("Installed (as dependency)", minst);

	def _update_model_installed_man(self):
		pacman = Pacman.Instance();
		minst = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_installed_pkgs(manual=True):
			for r in pacman.get_repos():
				spkg = pacman.get_package(r,pkg.name)
				if spkg:
					break
			minst.append(self._pkgview._pkg_to_model(spkg, pkg))
		self._pkgview.add_pkg_model("Installed (manual)", minst);

	def _update_model_installed_loc(self):
		pacman = Pacman.Instance();
		minst = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_installed_pkgs(localonly=True):
			minst.append(self._pkgview._pkg_to_model(None, pkg))
		self._pkgview.add_pkg_model("Installed (local)", minst);

	def _update_model_not_installed(self):
		pacman = Pacman.Instance();
		minst = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_not_installed():
			minst.append(self._pkgview._pkg_to_model(pkg))
		self._pkgview.add_pkg_model("Not Installed", minst);

	def _update_model_upgradeable(self):
		pacman = Pacman.Instance();
		mupgr = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
		for pkg in pacman.get_upgradeable():
			for r in pacman.get_repos():
				spkg = pacman.get_package(r,pkg.name)
				if spkg: break
			mupgr.append(self._pkgview._pkg_to_model(spkg, pkg))
		self._pkgview.add_pkg_model("Upgradeable", mupgr);

	def _update_model_all_and_grps(self):
		pacman = Pacman.Instance();
		mall = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)

		for repo in pacman.get_repos():
			mrep = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
			for pkg in pacman.get_package_list(repo):
				lpkg = pacman.get_local_package(pkg.name)
				mall.append(self._pkgview._pkg_to_model(pkg, lpkg))
				mrep.append(self._pkgview._pkg_to_model(pkg, lpkg))
			mrep.set_sort_column_id(2, Gtk.SortType.ASCENDING)
			self._pkgview.add_pkg_model(repo, mrep);

			for group in pacman.get_groups_of_repo(repo):
				mgrp = Gtk.ListStore(str,GdkPixbuf.Pixbuf,str,str,str,str)
				for pkg in pacman.get_package_list(repo, group):
					lpkg = pacman.get_local_package(pkg.name)
					mgrp.append(self._pkgview._pkg_to_model(pkg, lpkg))
				mgrp.set_sort_column_id(2, Gtk.SortType.ASCENDING)
				self._pkgview.add_pkg_model(group, mgrp)

		mall.set_sort_column_id(2, Gtk.SortType.ASCENDING)
		self._pkgview.add_pkg_model("All", mall);

	def _tv_selection_changed(self, selection):
		model,it = selection.get_selected()
		if it:
			entry = model[it][0]
			self._pkgview.set_package_model(entry)

	def _update_selected_model(self):
		model,it = self._treeview.get_selection().get_selected()
		if it:
			entry = model[it][0]
			self._pkgview.set_package_model(entry)

	def _on_g_button(self, b):
		self._treeview.set_model(self._group_lst)
		b.set_active(True)
		self._update_button_states(b)

	def _on_s_button(self, b):
		self._treeview.set_model(self._state_lst)
		b.set_active(True)
		self._update_button_states(b)

	def _on_r_button(self, b):
		self._treeview.set_model(self._repos_lst)
		b.set_active(True)
		self._update_button_states(b)

	def _on_f_button(self, b):
		self._treeview.set_model(self._filters_lst)
		b.set_active(True)
		self._update_button_states(b)

	def _on_sr_button(self, b):
		self._treeview.set_model(self._searches_lst)
		b.set_active(True)
		self._update_button_states(b)

	def _update_button_states(self, b):
		for but in self._button_grid.get_children():
			if but != b:
				but.set_active(False)


	def _add_buttons(self, button_grid):
		g_button = Gtk.ToggleButton("Groups", hexpand=True)
		s_button = Gtk.ToggleButton("Status", hexpand=True)
		r_button = Gtk.ToggleButton("Repos", hexpand=True)
		f_button = Gtk.ToggleButton("Filters", hexpand=True)
		sr_button= Gtk.ToggleButton("Search Results", hexpand=True)
		#a_button = Gtk.ToggleButton("Architecture", hexpand=True)
		g_button.connect("released", self._on_g_button)
		s_button.connect("released", self._on_s_button)
		r_button.connect("released", self._on_r_button)
		f_button.connect("released", self._on_f_button)
		sr_button.connect("released", self._on_sr_button)
		#a_button.connect("toggled", self._on_a_button)
		g_button.set_active(True)
		button_grid.add(g_button)
		button_grid.add(s_button)
		button_grid.add(r_button)
		button_grid.add(f_button)
		button_grid.add(sr_button)
		#button_grid.add(a_button)
