import pymongo
from pymongo import errors
import bson
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tela_sobre import Sobre


class ModuloBase(object):

    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        builder = Gtk.Builder()
        builder.add_from_file('tela_base.glade')
        self.tela_base = builder.get_object('tela_base')
        self.statusbar_base = builder.get_object('statusbar_base')

        # self.client, self.db, self.coll_usuarios = self.connect_db()
        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_nova_analise_prescricao_activate": self.func_abrir_tela_nova_analise_prescricao,
                                 "on_abrir_analise_prescricao_activate": self.func_abrir_tela_abrir_analise_prescricao,
                                 "on_cadastro_morador_activate": self.func_abrir_tela_cadastro_morador,
                                 "on_cadastro_medicamento_activate": self.func_abrir_tela_cadastro_medicamento,
                                 "on_historico_analise_prescricao_activate":
                                     self.func_abrir_tela_historico_analise_prescricao,
                                 "on_historico_cadastro_morador_activate":
                                     self.func_abrir_tela_historico_cadastro_morador,
                                 "on_historico_cadastro_medicamento_activate":
                                     self.func_abrir_tela_historico_cadastro_medicamento,
                                 "on_historico_opcoes_definicoes_activate":
                                     self.func_abrir_tela_historico_opcoes_definicoes,
                                 "on_historico_opcoes_usuario_activate": self.func_abrir_tela_historico_opcoes_usuario,
                                 "on_historico_gerenciamento_permissoes_activate":
                                     self.func_abrir_tela_historico_gerenciamento_permissoes,
                                 "on_opcoes_definicoes_activate": self.func_abrir_tela_opcoes_definicoes,
                                 "on_opcoes_meu_usuario_activate": self.func_abrir_tela_opcoes_meu_usuario,
                                 "on_opcoes_gerenciamento_permissoes_activate":
                                     self.func_abrir_tela_opcoes_gerenciamento_permissoes,
                                 "on_ajuda_documentacao_activate": self.func_abrir_tela_ajuda_documentacao,
                                 "on_ajuda_sobre_activate": self.func_abrir_tela_sobre})

        self.statusbar_base.push(self.statusbar_base.get_context_id('info'), 'Bem-vindo(a)!')

        self.tela_base.show_all()

    def func_analisa_permissoes(self):
        pass

    def func_abrir_tela_nova_analise_prescricao(self):
        pass

    def func_abrir_tela_abrir_analise_prescricao(self):
        pass

    def func_abrir_tela_cadastro_morador(self):
        pass

    def func_abrir_tela_cadastro_medicamento(self):
        pass

    def func_abrir_tela_historico_analise_prescricao(self):
        pass

    def func_abrir_tela_historico_cadastro_morador(self):
        pass

    def func_abrir_tela_historico_cadastro_medicamento(self):
        pass

    def func_abrir_tela_historico_opcoes_definicoes(self):
        pass

    def func_abrir_tela_historico_opcoes_usuario(self):
        pass

    def func_abrir_tela_historico_gerenciamento_permissoes(self):
        pass

    def func_abrir_tela_opcoes_definicoes(self):
        pass

    def func_abrir_tela_opcoes_meu_usuario(self):
        pass

    def func_abrir_tela_opcoes_gerenciamento_permissoes(self):
        pass

    def func_abrir_tela_ajuda_documentacao(self):
        pass

    def func_abrir_tela_sobre(self, widget):
        tela_sobre = Sobre(self.tela_base)
        print('func_abrir_tela_sobre', tela_sobre, widget)
