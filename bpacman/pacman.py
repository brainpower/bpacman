
# Copyright (C) 2013 anonymous <brainpower@gulli.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, re, traceback

import pyalpm
from pycman import config
from bpacman.singleton import *

@Singleton
class Pacman(object):

	def __init__(self):
		self.handle  = config.init_with_config("/etc/pacman.conf")
		self.handle.dlcb = self._cb_dl
		self.handle.eventcb = self._cb_event
		self.handle.questioncb = self._cb_conv
		self.handle.progresscb = self._cb_progress

		# for callbacks
		self._last_percent = 100
		self._last_i = -1

		self.update_members()

		self._to_install = set()
		self._to_upgrade = set()
		self._to_remove  = set()
		self._to_install_dep = set()
		self._to_upgrade_dep = set()
		self._to_remove_dep  = set()

	def update_members(self):
		self.syncdbs     = { p.name:p for p in self.handle.get_syncdbs() }
		self.repos       = [ p.name   for p in self.handle.get_syncdbs() ]
		self.groupcaches = [ (db,self.syncdbs[db].grpcache) for db in self.syncdbs ]
		self.groups      = { gc[0]:[ g[0]      for g in gc[1]] for gc in self.groupcaches }
		self.group_pkgs  = { gc[0]:{ g[0]:g[1] for g in gc[1]} for gc in self.groupcaches }
		self.all_pkg     = [ p for repo in self.handle.get_syncdbs() for p in repo.pkgcache]
		self.all_pkg_n   = [ p.name for repo in self.handle.get_syncdbs() for p in repo.pkgcache]
		self.upgradable_n= [ p.name for p in self.handle.get_localdb().pkgcache if pyalpm.sync_newversion(p, self.handle.get_syncdbs())]
		self.upgradable  = [ p for p in self.handle.get_localdb().pkgcache if pyalpm.sync_newversion(p, self.handle.get_syncdbs())]
		self.localpkgs_n = [ p.name for p in self.handle.get_localdb().pkgcache ]

	def mark_for_install(self, pkg, revert=False):
		if revert:
			self._to_install.remove(pkg)
		else:
			self._to_install.add(pkg)
		self.update_depend_inst(pkg, revert)

	def mark_for_upgrade(self, pkg, revert=False):
		if revert:
			self._to_upgrade.remove(pkg)
		else:
			self._to_upgrade.add(pkg)
		self.update_depend_upgr(pkg, revert)

	def mark_for_remove(self, pkg, revert=False):
		if revert:
			self._to_remove.remove(pkg)
		else:
			if not self.pkg_required(pkg):
				self._to_remove.add(pkg)
			else:
				return "error"
		#self.mark_depend_rem(pkg, revert)

	def unmark(self, pkgname):
		if pkgname in self._to_install:
			self.mark_for_install(pkgname,True)
		elif pkgname in self._to_upgrade:
			self.mark_for_upgrade(pkgname,True)
		elif pkgname in self._to_remove:
			self.mark_for_remove(pkgname,True)

	def update_depend_inst(self):
		self._to_install_dep = []
		for p in self._to_install:
			self._to_install_dep.append(self.get_depends(p))

	def update_depend_upgr(self, pkg, revert=False):
		self._to_upgrade_dep = []
		for p in self._to_upgrade:
			self._to_upgrade_dep.append(self.get_depends_n(p))

	#~ def mark_depend_rem(self, pkg, revert=False):
		#~ self._to_remove_dep = []
		#~ for p in self._to_remove:
			#~ if not self.pkg_required(p)
				#~ self._to_remove_dep.append(self.get_depends(p))

	def reset_marks(self ):
		self._to_install.clear()
		self._to_upgrade.clear()
		self._to_remove.clear()
		self._to_install_dep.clear()
		self._to_upgrade_dep.clear()
		self._to_remove_dep.clear()

	def get_to_install(self):
		return self._to_install
	def get_to_upgrade(self):
		return self._to_upgrade
	def get_to_remove(self):
		return self._to_remove
	def get_to_install_dep(self):
		return self._to_install_dep
	def get_to_upgrade_dep(self):
		return self._to_upgrade_dep
	#def get_to_remove_dep(self):

	def set_pcb(self, pcb):
		self.handle.progresscb = pcb

	def get_pcb(self):
		return self.handle.progresscb

	def set_dlcb(self, dlcb):
		self.handle.dlcb = dlcb

	def get_dlcb(self):
		return self.handle.dlcb

	def get_repos(self):
		return self.repos

	def get_groups(self):
		return self.groups

	def get_depends_n(self, pkgname):
		if len(pkgname.split("/")) > 1:
			repo,pkgn = pkgname.split("/")
			pkg = self.get_package(repo,pkgn)
			if pkg:
				return [ self.get_pkg_name_of_depend_name(p) for p in pkg.depends]

		for repo in self.get_repos():
			pkg = self.get_package(repo,pkgname)
			if pkg:
				return [ self.get_pkg_name_of_depend_name(p) for p in pkg.depends]

	def get_package(self, repo, pkgname):
		if repo == "local":
			return self.handle.get_localdb().get_pkg(pkgname)
		return self.syncdbs[repo].get_pkg(pkgname)

	def is_installed_n(self, pkgname):
		return pkgname in self.localpkgs_n

	def is_installed(self, pkg):
		return [p for p in self.handle.get_localdb().pkgcache if pkg.name == p.name]

	def get_not_installed(self):
		return [ p for p in self.all_pkg if not self.is_installed(p) ]

	def get_installed_pkgs(self, asdep=False, manual=False, localonly=False):
		if asdep:
			return [ p for p in self.handle.get_localdb().pkgcache if p.reason == 1 ]
		if manual:
			return [ p for p in self.handle.get_localdb().pkgcache if p.reason == 0 ]
		if localonly:
			return [x for x in self.handle.get_localdb().pkgcache if x.name not in self.all_pkg_n ]
		return self.handle.get_localdb().pkgcache

	def get_upgradeable(self):
		return self.upgradable

	def get_upgradeable_n(self):
		return self.upgradable_n

	def get_local_package(self, pkgname):
		return self.handle.get_localdb().get_pkg(pkgname)

	def get_package_list_nvd(self, repo, group=None):
		if not group:
			return [ (p.name, p.version, p.desc) for p in self.syncdbs[repo].pkgcache]
		else:
			return [ (p.name, p.version, p.desc) for p in self.group_pkgs[repo][group]]

	def get_package_list_n(self, repo, group=None):
		if not group:
			return [ { p.name : p} for p in self.syncdbs[repo].pkgcache]
		else:
			return [ { p.name : p} for p in self.group_pkgs[repo][group]]

	def get_package_list(self, repo, group=None):
		if not group:
			return self.syncdbs[repo].pkgcache
		else:
			return self.group_pkgs[repo][group]

	def get_repos_of_group(self, group):
		return [repo for repo in self.groups if group in self.groups[repo]]

	def get_groups_of_repo(self, repo):
		return self.groups[repo];

	def get_repos_of_pkg(self, pkg):
		return [ repo for repo in self.repos if self.get_package(repo, pkg) ]

	def get_groups_of_pkg(self, pkg):
		for repo in self.get_repos():
			return self.get_package(repo, pkg).groups;

	def update_dbs(self, force=False): # do a "pacman -Sy"
		print(self.handle.progresscb)
		print(self.handle.dlcb)
		for db in self.handle.get_syncdbs():
			t = self._t_init_from_options(None)
			db.update(force)
			t.release()
		self.update_members()

	def apply_marked(self):
		print("[pacman] Applying changes... please don't wait, not implemented yet")

	# default Callbacks
	def _cb_event(self, *args):
		print("event", args)

	def _cb_conv(self, *args):
		print("conversation", args)

	def _cb_progress(self, target, percent, n, i):
		"""Display progress percentage for target i/n"""
		if len(target) == 0:
			# abstract progress
			if percent < self._last_percent or i < self._last_i:
				sys.stdout.write("progress (%d targets)" % n)
				self._last_i = 0
			sys.stdout.write((i - last_i) * '.')
			sys.stdout.flush()
			self._last_i = i
		else:
			# progress for some target (write 25 dots for 100%)
			if target != self._last_target or percent < self._last_percent:
				self._last_target = target
				self._last_percent = 0
				sys.stdout.write("progress for %s (%d/%d)" % (target, i, n))
			old_dots = self._last_percent // 4
			new_dots = percent // 4
			sys.stdout.write((new_dots - old_dots) * '.')
			sys.stdout.flush()

		# final newline
		if percent == 100 and self._last_percent < 100:
			sys.stdout.write('\n')
			sys.stdout.flush()
		self._last_percent = percent

	def _cb_dl(self, filename, tx, total):
		# check if a new file is coming
		if filename != self._last_dl_filename or self._last_dl_total != total:
			self._last_dl_filename = filename
			self._last_dl_total = total
			self._last_dl_progress = 0
			sys.stdout.write("\ndownload %s: %d/%d" % (filename, tx, total))
			sys.stdout.flush()
		# compute a progress indicator
		if self._last_dl_total > 0:
			progress = (tx * 25) // self._last_dl_total
		else:
			# if total is unknown, use log(kBytes)²/2
			progress = int(math.log(1 + tx / 1024) ** 2 / 2)
		if progress > self._last_dl_progress:
			self._last_dl_progress = progress
			sys.stdout.write("\rdownload %s: %s %d/%d" % (filename, '.' * progress, tx, total))
			sys.stdout.flush()

	def _t_init_from_options(self, options):
		"""Transaction initialization"""

		return self.handle.init_transaction(
				cascade = getattr(options, "cascade", False),
				nodeps = getattr(options, "nodeps", False),
				force = getattr(options, 'force', False),
				dbonly = getattr(options, 'dbonly', False),
				downloadonly = getattr(options, 'downloadonly', False),
				nosave = getattr(options, 'nosave', False),
				recurse = (getattr(options, 'recursive', 0) > 0),
				recurseall = (getattr(options, 'recursive', 0) > 1),
				unneeded = getattr(options, 'unneeded', False),
				alldeps = (getattr(options, 'mode', None) == pyalpm.PKG_REASON_DEPEND),
				allexplicit = (getattr(options, 'mode', None) == pyalpm.PKG_REASON_EXPLICIT))

	def _t_finalize(self, t):
		"""Commit a transaction"""
		try:
			t.prepare()
			t.commit()
		except pyalpm.error:
			traceback.print_exc()
			t.release()
			return False
		t.release()
		return True

	@staticmethod
	def get_newest_of(pkglist):
		if pkglist:
			newest = pkglist[0]
			for pkg in pkglist:
				if 1 == pyalpm.vercmp(pkg.version, newest.version):
					newest = pkg
			return newest

	def get_pkg_name_of_depend_name(self, depname):
		return pyalpm.find_satisfier(self.all_pkg, depname).name


def main():
	#~ devs = get_devices()
	#~ for dev,typ in devs:
		#~ print(dev,typ)
	#print(get_filesystem_types())
	pacman = Pacman.Instance()
	#~ print(pacman.get_repos())
	#~ print(pacman.get_package_list("core"))
	#print(pacman.get_groups())
	#print(pacman.get_package_list("core", "base"))
	#print(pacman.get_repo_of_group("unity"))
	print(pacman.get_package("testing", "linux").installdate)
	print(pacman.get_package("local", "linux").installdate)
	print(pacman.get_package("core", "linux-lts").installdate)
	print(pacman.is_installed_n("linux"))
	print(pacman.is_installed_n("linux-lts"))


if __name__ == "__main__":
	main()
