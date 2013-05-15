from gi.repository import Gtk
from bpacman.actiondialog import *

class UpdateActionDialog(ActionDialog):
		#FIXME: dialog closes when delete came while closing being locked,
		#I want it to stay open till the user clicks X after this here
		# so i'm looking for a way to discard all previous events before disconnecting my lambda

	def __init__(self, parent, force=False):
		ActionDialog.__init__(self, "Updating databases...", parent)
		self._p = parent
		self._force = force
		self._qid = self.connect("delete-event", lambda x,y: True) # disable closing the dialog till we're done
		self.set_size_request(400,300)

		box = self.get_content_area()
		self._model = Gtk.ListStore(str,int)

		pacman = Pacman.Instance()

		#~ for repo in pacman.get_repos():
			#~ self._model.append([repo, 0])

		text = Gtk.TreeViewColumn("Repository", Gtk.CellRendererText(), text=0)
		progress = Gtk.TreeViewColumn("Progress", Gtk.CellRendererProgress(), value=1, inverted=2)

		tv = Gtk.TreeView(self._model)
		tv.append_column(text)
		tv.append_column(progress)

		tv.set_vexpand(True)
		sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
		sw.add(tv)
		box.add(sw)
		box.show_all()
		#self.show_all()

	def _run_action(self):
		pacman = Pacman.Instance()
		pacman.set_dlcb( self._progresscb)

		pacman.update_dbs(self._force)

		datastr = "updating package data"
		self._model.append([datastr, 0])
		self._p._pkgv._pkglist.update_models()
		self._progresscb(datastr, 50, 100);
		self._p._pkgv._sidebar._update_state_models()
		self._progresscb(datastr, 100, 100);

		self._close.set_sensitive(True)
		self.disconnect(self._qid) # reenable closing the dialog,

	def _progresscb(self, filename, PW, GW):
		for row in self._model:
			if row[0] == filename.split('.')[0]:
				row[1] = 100/GW*PW
				return
		if len(self._model) > 0:
			self._model[len(self._model)-1][1] = 100
		self._model.append([filename.split('.')[0], 100/GW*PW])
		for row in self._model:
			if row[0] == filename.split('.')[0]:
				row[1] = 100/GW*PW
				return
