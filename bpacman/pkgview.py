
from bpacman.sidebar import *
from bpacman.pkglistanddesc import *
from bpacman.pacman import *
from bpacman.updateactiondialog import *
from bpacman.applyactiondialog import *
from gi.repository import Polkit

class PkgView(Gtk.Paned):

	def __init__(self, parent, *args):
		Gtk.Paned.__init__(self, margin=4, *args);
		self._parent = parent

		self.set_orientation(Gtk.Orientation.HORIZONTAL);
		self.set_vexpand(True)

		self._pkglist = PkgListAndDesc(orientation=Gtk.Orientation.VERTICAL);
		self._sidebar = Sidebar(self._pkglist);

		self._sidebar.set_property("width-request", 180)

		self.add(self._sidebar);
		self.add(self._pkglist);

	def _reset_marks_action(self,x):
		pacman = Pacman.Instance()
		pacman.reset_marks()
		self._pkglist.update_models()

	def _mark_upgrades_action(self,x):
		pacman = Pacman.Instance()
		for pkg in pacman.get_upgradeable_n():
			pacman.mark_for_upgrade(pkg)
			self._pkglist.update_models(pkg)

	def _mark_pkg_inst_action(self, x):
		self._pkglist._mark_current_pkg_inst()

	def _mark_pkg_upgr_action(self, x):
		self._pkglist._mark_current_pkg_upgr()

	def _mark_pkg_rem_action(self, x):
		self._pkglist._mark_current_pkg_rem()

	def _unmark_pkg_action(self,x):
		self._pkglist._unmark_current_pkg()

	def _search_action(self,x):
		pass
		# open search dialog, get search options, create model, add it to _pkglist
		# make sidebar and _pkglist show the search

	#~ def _check_authorization_cb(self, authority, res, x):
		#~ try:
			#~ result = authority.check_authorization_finish(res)
			#~ if result.get_is_authorized():
				#~ print("Authorized")
#~
			#~ elif result.get_is_challenge():
				#~ print("Challenge")
			#~ else:
				#~ print("Not authorized")
		#~ except GObject.GError as error:
			#~ print("Error checking authorization: %s" % error.message)

	def _update_dbs_action(self, x):
		#auth = Polkit.Authority.get()
		#sbj = Polkit.UnixProcess.new(os.getppid())
		#action_id = "org.freedesktop.policykit.exec"

		dwin = UpdateActionDialog(self._parent)
		#auth.check_authorization(sbj, action_id, None, Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION, None, self._check_authorization_cb, dwin)

		dwin.start()
		dwin.run()
		dwin.join()
		dwin.destroy()


	def _apply_marks_action(self, x):
		dwin = ApplyActionDialog(self._parent)
		dwin.start()
		dwin.run()
		dwin.join()
		dwin.destroy()
