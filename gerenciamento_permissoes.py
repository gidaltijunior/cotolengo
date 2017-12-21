import datetime as dt
from pymongo import errors
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GerenciamentoPermissoes(object):

    def __init__(self, banco_dados, politica_tentativas_conexao):
        self.banco_dados = banco_dados
        self.politica_tentativas_conexao = politica_tentativas_conexao

        # TODO: definir as coleções apropriadas para essa tela
        # self.coll_usuarios = self.banco_dados['db'].usuarios

        builder = Gtk.Builder()
        builder.add_from_file('tela_gerenciamento_permissoes.glade')
        self.tela_gerenciamento_permissoes = builder.get_object('tela_gerenciamento_permissoes')

        '''
        self.lista_com_permissao = builder.get_object('lista_com_permissao')
        self.armazenamento_com_permissao = builder.get_object('armazenamento_com_permissao')
        self.coluna_com_permissao = Gtk.TreeViewColumn('Módulos com Permissão', Gtk.CellRendererText(), text=0)
        self.coluna_com_permissao.set_sort_column_id(0)
        self.lista_com_permissao.append_column(self.coluna_com_permissao)

        self.lista_sem_permissao = builder.get_object('lista_sem_permissao')
        self.armazenamento_sem_permissao = builder.get_object('armazenamento_sem_permissao')
        self.coluna_sem_permissao = Gtk.TreeViewColumn('Módulos sem Permissão', Gtk.CellRendererText(), text=0)
        self.coluna_sem_permissao.set_sort_column_id(0)
        self.lista_sem_permissao.append_column(self.coluna_sem_permissao)

        '''
        # TODO: Carregar as listas corretas para essa tela

        self.statusbar_gerenciamento_permissoes = builder.get_object('statusbar_gerenciamento_permissoes')

        # TODO: Ligar os sinais disponíveis no arquivo glade com as funções corretas

        builder.connect_signals({
            'on_fechar_clicked': self.fechar
        })

        self.statusbar_gerenciamento_permissoes.push(
            self.statusbar_gerenciamento_permissoes.get_context_id('info'),
            'Alterar autorizações e permissões sem autorização é um grave risco de segurança das informações.')

        # TODO: Carregar os dados esperados ao abrir a tela

        self.tela_gerenciamento_permissoes.show_all()

    def fechar(self, widget):
        print('fechar', widget)
        self.tela_gerenciamento_permissoes.close()
