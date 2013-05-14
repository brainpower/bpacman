
from bpacman.pkgview import *
from bpacman.fastfilter import *


class MainWindow(Gtk.Window):

	def __init__(self, title):
		Gtk.Window.__init__(self, title=title);

		self.set_default_size(1024, 786)
		self._pacman = Pacman.Instance()

		ag = Gtk.ActionGroup("actions");

		self._pkgv = PkgView(self);
		self._add_menu_actions(ag);

		uiman = Gtk.UIManager();
		uiman.add_ui_from_string(UIINFO);
		uiman.insert_action_group(ag);

		menubar = uiman.get_widget("/MenuBar");
		toolbar = uiman.get_widget("/ToolBar");
		menubar.set_hexpand(True)
		toolbar.set_hexpand(True)
		toolbar.set_style(Gtk.ToolbarStyle.BOTH);

		grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL);


		grid.add(menubar);
		grid.add(toolbar);
		grid.add(self._pkgv);
		#grid.add(statusbar);

		self.add(grid);

	def _add_menu_actions(self, ag):

		ag.add_actions([ # menu actions
		#     name          stock  label       accel       ttip  callback
		    ("FileMenu",     None, "_File",     None,       None, None),
		    ("EditMenu",     None, "_Edit",     None,       None, None),
		    ("PkgMenu",      None, "_Package",  None,       None, None),
		    ("SettingsMenu", None, "_Settings", None,       None, None),
		    ("HelpMenu",     None, "_Help",     None,       None, None),
		])

		ag.add_actions([ # menuitem actions
		#    name        stock               label                     accel       ttip  callback
		  ("History",    None,              "_History...",              None,      None, None),
		  ("Quit",       Gtk.STOCK_QUIT,    "_Quit",                   "<Ctrl>Q", None, Gtk.main_quit),

		  ("Undo",       Gtk.STOCK_UNDO,    "_Undo",                   "<Ctrl>Z", None, None),
		  ("Redo",       Gtk.STOCK_REDO,    "_Redo",                   "<Ctrl>Y", None, None),
		  ("UnmarkAll",  None,              "U_nmark all",              None,      None, self._pkgv._reset_marks_action),
		  ("Search",     Gtk.STOCK_FIND,    "_Search...",              "<Ctrl>F", None, self._pkgv._search_action),
		  ("UpdateDBs",  Gtk.STOCK_REFRESH, "_Update Databases...",    "<Ctrl>R", None, self._pkgv._update_dbs_action),
		  ("MarkUpgrds", None,              "_Mark upgradeable",       "<Ctrl>G", None, self._pkgv._mark_upgrades_action),
		  ("ApplyMarked",Gtk.STOCK_APPLY,   "A_pply marked changes...","<Ctrl>P", None, self._pkgv._apply_marks_action),

		  ("Unmark",     None,              "U_nmark",                 "<Ctrl>N", None, self._pkgv._unmark_pkg_action),
		  ("MarkInstall",Gtk.STOCK_ADD,     "Mark for _installation",  "<Ctrl>I", None, self._pkgv._mark_pkg_inst_action),
		  ("MarkReinst" ,Gtk.STOCK_REFRESH, "Mark for _reinstallation", None,      None, None),
		  ("MarkUpgrade",None,              "Mark for _upgrade",       "<Ctrl>U", None, None),
		  ("MarkRemove", Gtk.STOCK_REMOVE,  "Mark for _removal",       "Delete",   None, None),
		  ("MarkPurge",  Gtk.STOCK_DELETE,  "Mark for _purge",         "<Shift>Delete",   None, None),
		  #("Configure",  None,              "_Configure...",            None,      None, None),
		  #("LoadChangelog", None,           "_Download changelog",      None,      None, None),
		  ("Properties", Gtk.STOCK_PROPERTIES, "_Properties...",        "<Alt>Return", None, None),
		  ("Repos",      None,              "_Repositories...",          None,     None, None),
		  ("Filters",    None,              "_Filters...",               None,     None, None),
		  ("Toolbar",    None,              "_Toolbar",                  None,     None, None),
		    ("Icons",      None,            "_Icons only",               None,     None, None),
		    ("Text",       None,            "_Text only",                None,     None, None),
		    ("TextBelow",  None,            "Text _below icons",         None,     None, None),
		    ("TextBeside", None,            "Text be_side icons",        None,     None, None),
		    ("Hide",       None,            "_Hide",                     None,     None, None),
		  ("Contents",   None,              "_Contents",                "F1",      None, None),
		  ("Introduction", None,            "_Introduction",             None,      None, None),
		  ("About",      None,              "_About",                    None,      None, None),
		])

		ag.add_toggle_actions([
		  ("LockVersion",Gtk.STOCK_DIALOG_AUTHENTICATION, "_Lock Version", None,   None, None),
		  ("AutoInst",   None,              "Automatically installed",  None,      None, None),
		])

		ag.add_action(FastFilterAction("FastFilter", "FastFilter", None, None));

		ag.get_action("MarkUpgrds") .set_icon_name("system-upgrade");
		ag.get_action("MarkUpgrade").set_icon_name("system-upgrade");
		ag.get_action("UnmarkAll")  .set_icon_name("revert");
		ag.get_action("Unmark")     .set_icon_name("revert");


UIINFO = """
<ui>
	<menubar name='MenuBar'>
		<menu action='FileMenu'>
			<menuitem action='History' />
			<separator />
			<menuitem action='Quit' />
		</menu>
		<menu action='EditMenu'>
			<menuitem action='Undo' />
			<menuitem action='Redo' />
			<menuitem action='UnmarkAll' />
			<separator />
			<menuitem action='Search' />
			<separator />
			<menuitem action='UpdateDBs' />
			<menuitem action='MarkUpgrds' />
			<!--<menuitem action='FixBroken' />-->
			<separator />
			<menuitem action='ApplyMarked' />
		</menu>
		<menu action='PkgMenu'>
			<menuitem action='Unmark' />
			<menuitem action='MarkInstall' />
			<menuitem action='MarkReinst' />
			<menuitem action='MarkUpgrade' />
			<menuitem action='MarkRemove' />
			<menuitem action='MarkPurge' />
			<separator />
			<menuitem action='LockVersion' />
			<menuitem action='AutoInst' />
			<!--<menuitem action='ForceVersion' />-->
			<!--<separator />-->
			<!--<menuitem action='Configure' />-->
			<!--<menuitem action='LoadChangelog' />-->
			<separator />
			<menuitem action='Properties' />
		</menu>
		<menu action='SettingsMenu'>
			<menuitem action='Properties' />
			<menuitem action='Repos' />
			<menuitem action='Filters' />
			<menu action='Toolbar'>
				<menuitem action='Icons' />
				<menuitem action='Text' />
				<menuitem action='TextBelow' />
				<menuitem action='TextBeside' />
				<menuitem action='Hide' />
			</menu>
		</menu>
		<menu action='HelpMenu' >
			<menuitem action='Contents' />
			<menuitem action='Introduction' />
			<menuitem action='About' />
		</menu>
	</menubar>
	<toolbar name='ToolBar'>
		<toolitem action='UpdateDBs' />
		<toolitem action='MarkUpgrds' />
		<toolitem action='ApplyMarked' />
		<separator />
		<toolitem action='Properties' />
		<separator />
		<toolitem action='FastFilter' />
		<separator />
		<toolitem action='Search' />
		<toolitem action='Quit' />
	</toolbar>
</ui>
"""
