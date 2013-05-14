import time, threading

from gi.repository import Gtk
from bpacman.pacman import *

class ActionDialog(Gtk.Dialog):

	class ActionThread(threading.Thread):
		def __init__(self, func):
			threading.Thread.__init__(self);
			self._func = func

		def run(self):
			self._func()

	def __init__(self, title, parent):
		Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL);

		self._close = self.add_button("Close", Gtk.ResponseType.CLOSE)
		self._close.set_sensitive(False);

		self._t = self.ActionThread(self._run_action)

	def start(self):
		self._t.start()

	def _run_action(self):
		raise NotImplementedError("You shall reimplement this class!")

	def join(self):
		self._t.join()
