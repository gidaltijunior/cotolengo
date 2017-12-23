import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Sobre(object):

    def __init__(self, parent_window):
        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_sobre.glade')
        self.tela_sobre = builder.get_object('tela_sobre')
        self.tela_sobre.set_transient_for(parent_window)

        self.tela_sobre.show_all()
