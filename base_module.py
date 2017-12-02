import pymongo
from pymongo import errors
import bson
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ModuloBase(object):

    def __init__(self):
        self.validacao_ok = False
        builder = Gtk.Builder()
        builder.add_from_file('tela_base.glade')
        self.tela_base = builder.get_object('tela_base')
        self.usuario = builder.get_object('usuario')
        self.senha = builder.get_object('senha')
        self.logar = builder.get_object('logar')
        self.criar_usuario = builder.get_object('criar_usuario')
        self.statusbar_login = builder.get_object('statusbar_login')

        # self.client, self.db, self.coll_usuarios = self.connect_db()
        builder.connect_signals({"gtk_main_quit": Gtk.main_quit})

        self.tela_base.show_all()
