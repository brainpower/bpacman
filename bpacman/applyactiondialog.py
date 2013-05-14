from gi.repository import Gtk
from bpacman.actiondialog import *

class ApplyActionDialog(ActionDialog):

	def __init__(self, parent):
		ActionDialog.__init__(self, "Downloading packages...", parent)
		self._qid = self.connect("delete-event", lambda x,y: True) # disable closing the dialog till we're done
		self.set_size_request(800,300)

		box = self.get_content_area()
		self._dmodel = Gtk.ListStore(str,int)
		self._imodel = Gtk.ListStore(str,int)
		self._dling = True

		pacman = Pacman.Instance()

		text = Gtk.TreeViewColumn("Package", Gtk.CellRendererText(), text=0)
		progress = Gtk.TreeViewColumn("Progress", Gtk.CellRendererProgress(), value=1, inverted=2)

		self._tv = Gtk.TreeView(self._dmodel)
		self._tv.append_column(text)
		self._tv.append_column(progress)

		#box.add()
		box.add(self._tv)
		box.show_all()

	def _run_action(self):
		pacman = Pacman.Instance()
		pacman.set_dlcb( self._dlcb)
		pacman.set_evcb( self._evcb)
		pacman.set_pcb( self._prgcb)

		pacman.apply_marked()

		datastr = "updating package data"
		self._model.append([datastr, 0])
		self._p._pkgv._pkglist.update_models()
		self._progresscb(datastr, 50, 100);
		self._p._pkgv._sidebar._update_state_models()
		self._progresscb(datastr, 100, 100);


		self._close.set_sensitive(True)
		self.disconnect(self._qid) # reenable closing the dialog,

	def _evcb(self, num, text, x):
		print("ev", num, text, x)
		self._lastev = text

	def _dlcb(self, filename, PW, GW):
		for row in self._dmodel:
			if filename == row[0]:
				row[1] = 100/GW*PW
				return
		self._dmodel.append([filename, 100/GW*PW])

	def _prgcb(self, targ, p, tnum, num):
		if targ:
			if self._dling: # assume this is called if download is done? so change some things on first call of this
				self.set_title("Installing packages...")
				self._tv.set_model(self._imodel)
				self._dling = False

			for row in self._imodel:
				if targ == row[0]:
					row[1] = p
					return
			self._imodel.append([targ, p])
			for row in self._imodel:
				if targ == row[0]:
					row[1] = p
					return
		else:
			for row in self._imodel:
				if self._lastev == row[0]:
					row[1] = p
					return
			self._imodel.append([self._lastev, p])
