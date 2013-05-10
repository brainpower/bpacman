
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

import os, re

import pyalpm
from pycman import config, transaction
from bpacman.singleton import *

@Singleton
class Pacman(object):

	def __init__(self):
		self.handle  = config.init_with_config("/etc/pacman.conf")
		self.update_members()


	def update_members(self):
		self.syncdbs     = { p.name:p for p in self.handle.get_syncdbs() }
		self.repos       = [ p.name   for p in self.handle.get_syncdbs() ]
		self.groupcaches = [ (db,self.syncdbs[db].grpcache) for db in self.syncdbs ]
		self.groups      = { gc[0]:[ g[0]      for g in gc[1]] for gc in self.groupcaches }
		self.group_pkgs  = { gc[0]:{ g[0]:g[1] for g in gc[1]} for gc in self.groupcaches }
		self.all_pkg     = [ p for repo in self.handle.get_syncdbs() for p in repo.pkgcache]
		self.all_pkg_n   = [ p.name for repo in self.handle.get_syncdbs() for p in repo.pkgcache]

	def get_repos(self):
		return self.repos

	def get_groups(self):
		return self.groups

	def get_package(self, repo, pkgname):
		if repo == "local":
			return self.handle.get_localdb().get_pkg(pkgname)
		return self.syncdbs[repo].get_pkg(pkgname)

	def is_installed_n(self, pkgname):
		return pkgname in [ p.name for p in self.handle.get_localdb().pkgcache ]

	def is_installed(self, pkg):
		return pkg in self.handle.get_localdb().pkgcache

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
		return [ p for p in self.handle.get_localdb().pkgcache if pyalpm.sync_newversion(p, self.handle.get_syncdbs())]

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

	def update_dbs(self):
		for db in self.handle.get_syncdbs(): # do a -Sy on start
			t = transaction.init_from_options(self.handle, None)
			db.update(False) # dont force update
			t.release()
		self.update_members()

	@staticmethod
	def get_newest_of(pkglist):
		if pkglist:
			newest = pkglist[0]
			for pkg in pkglist:
				if 1 == pyalpm.vercmp(pkg.version, newest.version):
					newest = pkg
			return newest


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
