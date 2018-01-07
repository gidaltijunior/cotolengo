import datetime as dt
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class CadastroMorador(object):

    def __init__(self, usuario, banco_dados, politica_tentativas_conexao):

        self.usuario_logado = usuario
        self.banco_dados = banco_dados
        self.politica_tentativas_conexao = politica_tentativas_conexao
        self.coll_usuarios = self.banco_dados['db'].usuarios

        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_cadastro_morador.glade')

        self.tela_cadastro_morador = builder.get_object('tela_cadastro_morador')
        """
        self.usuario = builder.get_object('usuario')
        self.nome_completo = builder.get_object('nome_completo')
        self.email = builder.get_object('email')
        self.senha_atual = builder.get_object('senha_atual')
        self.nova_senha = builder.get_object('nova_senha')
        self.nova_senha_repetir = builder.get_object('nova_senha_repetir')
        self.atualizar_senha_botao = builder.get_object('atualizar_senha')
        self.data_criacao = builder.get_object('data_criacao')

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

        self.statusbar_meu_usuario = builder.get_object('statusbar_meu_usuario')

        builder.connect_signals({'on_atualizar_dados_clicked': self.atualizar_dados,
                                 'on_atualizar_senha_clicked': self.atualizar_senha,
                                 'on_senha_atual_key_release_event': self.validar_troca_senha,
                                 'on_nova_senha_key_release_event': self.validar_troca_senha,
                                 'on_nova_senha_repetir_key_release_event': self.validar_troca_senha,
                                 'on_fechar_clicked': self.fechar
                                 })

        self.statusbar_meu_usuario.push(
            self.statusbar_meu_usuario.get_context_id('info'),
            'Caso altere a senha, tome nota, pois será requisitada no próximo login.')

        self.carregar_definicoes()
        """

        self.tela_cadastro_morador.show_all()


    def carregar_definicoes(self):
        for retries in range(self.politica_tentativas_conexao):
            try:

                item = self.coll_usuarios.find_one({'usuario': self.usuario_logado})

                self.usuario.set_text(item['usuario'])
                self.nome_completo.set_text(item['nome'])
                self.email.set_text(item['e-mail'])

                data_solicitacao = item['data_solicitacao']
                data_solicitacao = str('{:%d/%m/%Y às %H:%M:%S}').format(data_solicitacao)
                self.data_criacao.set_text(data_solicitacao)

                lista_permissoes = item['permissoes']

                for item in lista_permissoes:
                    if lista_permissoes[item] is True:
                        self.armazenamento_com_permissao.append([item])
                    elif lista_permissoes[item] is False:
                        self.armazenamento_sem_permissao.append([item])

                self.atualizar_senha_botao.set_sensitive(False)

                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_meu_usuario.push(
                self.statusbar_meu_usuario.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def atualizar_dados(self, widget):
        print('atualizar_dados', widget)
        nome = self.nome_completo.get_text()
        email = self.email.get_text()
        for retries in range(self.politica_tentativas_conexao):
            try:
                self.coll_usuarios.update({'usuario': self.usuario_logado}, {'$set': {'nome': nome, 'e-mail': email}})
                self.statusbar_meu_usuario.push(
                    self.statusbar_meu_usuario.get_context_id('info'),
                    'Dados atualizados com sucesso!')
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_meu_usuario.push(
                self.statusbar_meu_usuario.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def atualizar_senha(self, widget):
        print('atualizar_senha', widget)
        for retries in range(self.politica_tentativas_conexao):
            try:
                senha_atual = CriarUsuario.hash_password(self.senha_atual.get_text())
                senha_nova = CriarUsuario.hash_password(self.nova_senha_repetir.get_text())

                item = self.coll_usuarios.find_one({'usuario': self.usuario_logado})
                senha_atual_db = item['senha']

                if senha_atual == senha_atual_db:
                    self.coll_usuarios.update({'usuario': self.usuario_logado}, {'$set': {'senha': senha_nova}})
                    self.statusbar_meu_usuario.push(
                        self.statusbar_meu_usuario.get_context_id('info'),
                        'Sua senha foi atualizada com sucesso! Não a esqueça.')
                else:
                    self.statusbar_meu_usuario.push(
                        self.statusbar_meu_usuario.get_context_id('info'),
                        'A senha atual não é a mesma cadastrada no banco de dados.')
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_meu_usuario.push(
                self.statusbar_meu_usuario.get_context_id('info'),
                'Não foi possível estabelecer uma conexão com o banco de dados.')

    def validar_troca_senha(self, widget, focus):  # valida o formulario para habilitar o botao 'enviar solicitacao'
        print(widget, focus)
        if self.nova_senha.get_text() == self.nova_senha_repetir.get_text() \
                and self.senha_atual.get_text() != self.nova_senha_repetir.get_text() \
                and len(str(self.nova_senha_repetir.get_text())) > 3 \
                and len(str(self.senha_atual.get_text())) > 3:
            self.atualizar_senha_botao.set_sensitive(True)
        else:
            self.atualizar_senha_botao.set_sensitive(False)

    def fechar(self, widget):
        print('fechar', widget)
        self.tela_meu_usuario.close()
