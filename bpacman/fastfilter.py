
from gi.repository import Gtk, GObject

class FastFilterAction(Gtk.Action):
	__gtype_name__ = "FastFilterAction"

	def __init__(self, *args):
		Gtk.Action.__init__(self, *args);

	def create_tool_item(self):
		ti = Gtk.ToolItem()
		entry = Gtk.Entry()
		entry.connect("activate", self.activate)
		ti.add(entry)
		return ti

#GObject.type_register(FastFilterAction)
