import pymongo
from pymongo import errors
import hashlib
import datetime as dt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DefinicoesAplicativo(object):

    def __init__(self, coll_definicoes_aplicativo):
        builder = Gtk.Builder()
        builder.add_from_file('tela_definicoes_aplicativo.glade')
        self.tela_definicoes_aplicativo = builder.get_object('tela_definicoes_aplicativo')

        self.tela_definicoes_aplicativo.show_all()
