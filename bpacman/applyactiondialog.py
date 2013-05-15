from gi.repository import Gtk,GLib,Gdk
from bpacman.actiondialog import *

class ApplyActionDialog(ActionDialog):

	def __init__(self, parent):
		ActionDialog.__init__(self, "Downloading packages...", parent)
		self._p = parent
		self._qid = self.connect("delete-event", lambda x,y: True) # disable closing the dialog till we're done
		self.set_size_request(900,400)

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
		self._tv.set_vexpand(True)

		#box.add()
		sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
		sw.add(self._tv)
		box.add(sw)
		box.show_all()

	def __run_action(self):
		for x in range(20):
			time.sleep(3)
			self._prgcb("test", 100/20*x, 0,0)
		self._close.set_sensitive(True)

	def _run_action(self):
		pacman = Pacman.Instance()
		pacman.set_dlcb( self._dlcb)
		pacman.set_evcb( self._evcb)
		pacman.set_pcb( self._prgcb)

		pacman.apply_marked()

		datastr = "updating package data"
		self._imodel.append([datastr, 0])
		self._p._pkgv._pkglist.update_models()
		self._prgcb(datastr, 50, 0, 0);
		self._p._pkgv._sidebar._update_state_models()
		self._prgcb(datastr, 100, 0, 0);


		self._close.set_sensitive(True)
		self.disconnect(self._qid) # reenable closing the dialog,

	def _evcb(self, num, text, x):
		print("ev", num, text, x)
		self._lastev = text
		if num == 1 or num == 2:
			print("ev", num, text, x)

		# statuses, e.g. file conflicts, integrity, etc
		elif num in (3, 19, 23, 36,):
			# event no. 3: "file conflicts", 19 "integrity", 21 "load pkg", 36 "keyring"
			self._ndlastev = text
			if num == 36: # FIXME: pyalpm prints "unknown event"
				self.lastev = "keyring check"
				self._ndlastev = self.lastev

			if len(self._imodel) > 0:
				self._imodel[0] = [self._lastev, 0]
			else:
				self._imodel.append([self._lastev, 0])
				if self._dling: # assume this is called if download is done, so change some things on first call of this event
					self.set_title("Installing packages...")
					self._tv.set_model(self._imodel)
					self._dling = False
		elif num in (4, 20, 24, 37,): # event "Done"s for above events
			self._imodel[0] = [self._ndlastev, 100]

		# packages
		elif num in (9, 11, 13, 15, 17):
			# event no. 9: "Adding a package", no. 11: "removing", no. 13 "upgrading", 15 "downgrade", 17 "reinstall"
			self._imodel.append([x[1].name, 0])
			self._tv.set_model(self._imodel)
			if self._dling: # assume this is called if download is done, so change some things on first call of this event
				self.set_title("Installing packages...")
				self._tv.set_model(self._imodel)
				self._dling = False
		elif num in (10, 12, 14, 16, 18): # event "Done"s for above events
			for row in self._imodel:
				if x[1].name == row[0]:
					row[1] = 100

		# TODO: deltas

	def _dlcb(self, filename, PW, GW):
		for row in self._dmodel:
			if filename == row[0]:
				row[1] = 100/GW*PW
				return
		self._dmodel.append([filename, 100/GW*PW])

	def _prgcb(self, targ, p, tnum, num):
		print("prgcb",targ,p, self._dling)
		if targ != "":
			for row in self._imodel:
				if targ == row[0]:
					row[1] = p
					return
		else:
			for row in self._imodel:
				if self._lastev == row[0]:
					row[1] = p
					return


if __name__ == "__main__":
	GLib.threads_init()
	Gdk.threads_init()
	Gdk.threads_enter()
	dwin = ApplyActionDialog(None)
	dwin.start()
	dwin.run()
	dwin.join()
	dwin.destroy()
	Gdk.threads_leave()
