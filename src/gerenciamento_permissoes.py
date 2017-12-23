import datetime as dt
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GerenciamentoPermissoes(object):

    def __init__(self, banco_dados, politica_tentativas_conexao):
        self.banco_dados = banco_dados
        self.politica_tentativas_conexao = politica_tentativas_conexao

        self.coll_usuarios = self.banco_dados['db'].usuarios

        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_gerenciamento_permissoes.glade')
        self.tela_gerenciamento_permissoes = builder.get_object('tela_gerenciamento_permissoes')
        self.botao_autorizar = builder.get_object('autorizar')
        self.botao_desautorizar = builder.get_object('desautorizar')

        self.botao_desautorizar.set_sensitive(False)
        self.botao_autorizar.set_sensitive(False)

        self.lista_desautorizados = builder.get_object('lista_desautorizados')
        self.armazenamento_desautorizados = builder.get_object('armazenamento_desautorizados')
        self.coluna_desautorizados_usuario = Gtk.TreeViewColumn('Usuário', Gtk.CellRendererText(), text=0)
        self.coluna_desautorizados_nome = Gtk.TreeViewColumn('Nome', Gtk.CellRendererText(), text=1)
        self.coluna_desautorizados_email = Gtk.TreeViewColumn('E-mail', Gtk.CellRendererText(), text=2)
        self.coluna_desautorizados_datasolicitacao = Gtk.TreeViewColumn('Data Solicitação', Gtk.CellRendererText(),
                                                                        text=3)
        self.coluna_desautorizados_usuario.set_sort_column_id(0)
        self.lista_desautorizados.append_column(self.coluna_desautorizados_usuario)
        self.lista_desautorizados.append_column(self.coluna_desautorizados_nome)
        self.lista_desautorizados.append_column(self.coluna_desautorizados_email)
        self.lista_desautorizados.append_column(self.coluna_desautorizados_datasolicitacao)
        self.visao_arvore_desautorizados = builder.get_object('visao_arvore_desautorizados')

        self.lista_autorizados = builder.get_object('lista_autorizados')
        self.armazenamento_autorizados = builder.get_object('armazenamento_autorizados')
        self.coluna_autorizados_usuario = Gtk.TreeViewColumn('Usuário', Gtk.CellRendererText(), text=0)
        self.coluna_autorizados_nome = Gtk.TreeViewColumn('Nome', Gtk.CellRendererText(), text=1)
        self.coluna_autorizados_email = Gtk.TreeViewColumn('E-mail', Gtk.CellRendererText(), text=2)
        self.coluna_autorizados_datasolicitacao = Gtk.TreeViewColumn('Data Solicitação', Gtk.CellRendererText(), text=3)
        self.coluna_autorizados_usuario.set_sort_column_id(0)
        self.lista_autorizados.append_column(self.coluna_autorizados_usuario)
        self.lista_autorizados.append_column(self.coluna_autorizados_nome)
        self.lista_autorizados.append_column(self.coluna_autorizados_email)
        self.lista_autorizados.append_column(self.coluna_autorizados_datasolicitacao)
        self.visao_arvore_autorizados = builder.get_object('visao_arvore_autorizados')

        self.lista_usuarios = builder.get_object('lista_usuarios')
        self.armazenamento_usuarios = builder.get_object('armazenamento_usuarios')
        self.coluna_usuarios = Gtk.TreeViewColumn('Usuário', Gtk.CellRendererText(), text=0)
        self.coluna_usuarios.set_sort_column_id(0)
        self.lista_usuarios.append_column(self.coluna_usuarios)

        self.statusbar_gerenciamento_permissoes = builder.get_object('statusbar_gerenciamento_permissoes')

        builder.connect_signals({
            'on_fechar_clicked': self.fechar,
            'on_lista_desautorizados_cursor_changed': self.desautorizado_selecionado,
            'on_lista_autorizados_cursor_changed': self.autorizado_selecionado,
            'on_autorizar_clicked': self.autorizar,
            'on_desautorizar_clicked': self.desautorizar,
            'on_lista_usuarios_cursor_changed': self.carregar_checkboxes,
            'on_salvar_clicked': self.salvar
        })

        self.statusbar_gerenciamento_permissoes.push(
            self.statusbar_gerenciamento_permissoes.get_context_id('info'),
            'Alterar autorizações e permissões sem autorização é um grave risco de segurança das informações.')

        self.carregar_usuarios()
        self.carregar_desautorizados()
        self.carregar_autorizados()

        self.tela_gerenciamento_permissoes.show_all()

    def autorizar(self, widget):
        print('autorizar', widget)
        selecao = self.lista_desautorizados.get_selection()
        modelo, iteracao = selecao.get_selected()
        valor = modelo.get_value(iteracao, 0)
        for retries in range(self.politica_tentativas_conexao):
            try:
                autorizados = self.coll_usuarios.update_one({'usuario': valor}, {'$set': {'autorizado': True}})
                print('autorizados', autorizados)
                self.carregar_desautorizados()
                self.carregar_autorizados()
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                    'O usuário \'{0}\' foi autorizado com sucesso.'.format(valor))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def autorizado_selecionado(self, widget):
        print('autorizado_selecionado', widget)
        self.botao_desautorizar.set_sensitive(True)
        self.botao_autorizar.set_sensitive(False)
        self.visao_arvore_desautorizados.unselect_all()

    def desautorizar(self, widget):
        print('desautorizar', widget)
        selecao = self.lista_autorizados.get_selection()
        modelo, iteracao = selecao.get_selected()
        valor = modelo.get_value(iteracao, 0)
        for retries in range(self.politica_tentativas_conexao):
            try:
                desautorizados = self.coll_usuarios.update_one({'usuario': valor}, {'$set': {'autorizado': False}})
                print('desautorizados', desautorizados)
                self.carregar_desautorizados()
                self.carregar_autorizados()
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                    'O usuário \'{0}\' foi desautorizado com sucesso.'.format(valor))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def desautorizado_selecionado(self, widget):
        print('desautorizado_selecionado', widget)
        self.botao_desautorizar.set_sensitive(False)
        self.botao_autorizar.set_sensitive(True)
        self.visao_arvore_autorizados.unselect_all()

    def salvar(self, widget):
        # TODO: Implementar Salvar
        pass

    def carregar_autorizados(self):
        for retries in range(self.politica_tentativas_conexao):
            try:
                self.armazenamento_autorizados.clear()
                valores = self.coll_usuarios.find({'autorizado': True})
                for valor in valores:
                    valor['data_solicitacao'] = str('{:%d/%m/%Y às %H:%M:%S}').format(valor['data_solicitacao'])
                    self.armazenamento_autorizados.append([valor['usuario'], valor['nome'], valor['e-mail'],
                                                           valor['data_solicitacao']])
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def carregar_desautorizados(self):
        for retries in range(self.politica_tentativas_conexao):
            try:
                self.armazenamento_desautorizados.clear()
                valores = self.coll_usuarios.find({'autorizado': False})
                for valor in valores:
                    valor['data_solicitacao'] = str('{:%d/%m/%Y às %H:%M:%S}').format(valor['data_solicitacao'])
                    self.armazenamento_desautorizados.append([valor['usuario'], valor['nome'], valor['e-mail'],
                                                              valor['data_solicitacao']])
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def carregar_usuarios(self):
        for retries in range(self.politica_tentativas_conexao):
            try:
                self.armazenamento_usuarios.clear()
                valores = self.coll_usuarios.find({})
                for valor in valores:
                    self.armazenamento_usuarios.append([valor['usuario']])
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def carregar_checkboxes(self, widget):
        # print('carregar_checkboxes', widget)
        # TODO: Implementar Carregar Checkboxes
        pass

    def fechar(self, widget):
        print('fechar', widget)
        self.tela_gerenciamento_permissoes.close()
