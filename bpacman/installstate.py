import sys,os.path
from bpacman.pacman import *
from gi.repository import GdkPixbuf

class InstState(object):

	_files = { "default"   : "package-available.png",
	           "installed" : "package-installed-updated.png",
	           "updateable": "package-installed-outdated.png",
	           "remove"    : "package-remove.png",
	           "install"   : "package-install.png",
	           "reinstall" : "package-reinstall.png",
	           "upgrade"   : "package-upgrade.png"}

	_searchpaths = [ sys.prefix + "/share/bpacman/",
	                 os.path.dirname(__file__) + "/../data/",]

	@staticmethod
	def get_icon_of_state(state):
		for path in InstState._searchpaths:
			filename = os.path.normpath( path+InstState._files[state])
			if os.path.exists(filename):
				return GdkPixbuf.Pixbuf.new_from_file(filename) # hardcoded for now, till I find a better solution

	@staticmethod
	def get_stateicon_of_pkg(pkgname):
		pacman = Pacman.Instance()
		state = "default"
		if pacman.is_installed_n(pkgname):
			state = "installed"
		if pkgname in pacman.get_upgradeable_n():
			state = "updateable"
		if pkgname in pacman.get_to_install() or pkgname in pacman.get_to_install_dep():
			state = "install"
		if pkgname in pacman.get_to_upgrade() or pkgname in pacman.get_to_upgrade_dep():
			state = "upgrade"
		if pkgname in pacman.get_to_remove():
			state = "remove"

		return InstState.get_icon_of_state(state)
