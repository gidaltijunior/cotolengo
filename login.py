import pymongo
from pymongo import errors
import hashlib
import datetime as dt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import base_module


class Login(object):

    def __init__(self):
        self.validacao_ok = False
        builder = Gtk.Builder()
        builder.add_from_file('tela_login.glade')
        self.tela_login = builder.get_object('tela_login')
        self.usuario = builder.get_object('usuario')
        self.senha = builder.get_object('senha')
        self.logar = builder.get_object('logar')
        self.criar_usuario = builder.get_object('criar_usuario')
        self.statusbar_login = builder.get_object('statusbar_login')

        self.client, self.db, self.coll_usuarios = self.connect_db()

        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_criar_usuario_clicked": self.func_criar_usuario,
                                 "on_logar_clicked": self.func_logar})

        self.tela_login.show_all()

    def connect_db(self):
        print('connect db')
        client, db, coll_usuarios = None, None, None
        for retries in range(3):
            try:
                client = pymongo.MongoClient('mongodb://localhost')
                db = client.get_database('cotolengo')
                coll_usuarios = db.usuarios
                client.server_info()
                self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'),
                                          'Conexão com banco de dados sucedida!')
                break
            except pymongo.errors.AutoReconnect:
                self.logar.set_sensitive(False)
                self.criar_usuario.set_sensitive(False)
                self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'),
                                          'Conexão com banco de dados falhou.')
                print('Banco de Dados não está disponível. Tentando novamente:', retries)
        return client, db, coll_usuarios

    def func_criar_usuario(self, widget):
        print('func_criar_usuario', widget)
        tela_criar_usuario = CriarUsuario(self.coll_usuarios)
        print('tela_criar_usuario.usuario_criado', tela_criar_usuario.usuario_criado)

    def func_logar(self, widget):
        print('func_logar', widget)
        item = self.coll_usuarios.find_one({'usuario': str(self.usuario.get_text()).lower()})
        if item is not None:
            if item['autorizado'] is True:
                new_hash = self.hash_password(self.senha.get_text())
                self.validacao_ok = self.compare_hashes(item['senha'], new_hash)
            else:
                self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                          'Usuário não autorizado.')
                return
        else:
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                      'Usuário não cadastrado.')
            return

        if self.validacao_ok is True:
            self.tela_login.hide()
            # NOVA JANELA VEM AQUI !!!!!!!!!!!!!!!!!!!!!!
        else:
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                      'Senha incorreta.')

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(str(password).encode()).hexdigest()

    @staticmethod
    def compare_hashes(stored_hash, new_hash):
        if stored_hash == new_hash:
            return True
        else:
            return False


class CriarUsuario(object):

    def __init__(self, usuarios_db):
        self.usuario_criado = False
        builder = Gtk.Builder()
        builder.add_from_file('tela_login.glade')
        self.tela_criar_usuario = builder.get_object('tela_criar_usuario')
        self.nome_completo = builder.get_object('nome_completo')
        self.nome_usuario = builder.get_object('nome_usuario')
        self.email = builder.get_object('email')
        self.senha_criar = builder.get_object('senha_criar')
        self.senha_repetir = builder.get_object('senha_repetir')
        self.cancelar = builder.get_object('cancelar')
        self.enviar_solicitacao = builder.get_object('enviar_solicitacao')
        self.statusbar_criar_usuario = builder.get_object('statusbar_criar_usuario')
        self.statusbar_login = builder.get_object('statusbar_login')

        self.usuarios_db = usuarios_db

        builder.connect_signals({"on_cancelar_clicked": self.func_cancelar,
                                 "on_enviar_solicitacao_clicked": self.func_enviar_solicitacao,
                                 "on_senha_criar_focus_out_event": self.func_comparar_senhas,
                                 "on_senha_repetir_focus_out_event": self.func_comparar_senhas})

        self.enviar_solicitacao.set_sensitive(False)

        self.tela_criar_usuario.show_all()

    def func_cancelar(self, widget):
        print('func_cancelar', widget)
        self.tela_criar_usuario.close()

    def func_enviar_solicitacao(self, widget):
        cursor = self.usuarios_db.find({})
        for item in cursor:
            if item['usuario'] == self.nome_usuario.get_text():
                self.statusbar_criar_usuario.push(self.statusbar_criar_usuario.get_context_id('criar_usuario'),
                                                  'Nome de usuário já existente. Escolha outro.')
                break
        else:
            self.usuarios_db.insert({
                "usuario": str(self.nome_usuario.get_text()).lower(),
                "nome": str(self.nome_completo.get_text()).title(),
                "e-mail": str(self.email.get_text()).lower(),
                "data_solicitacao": dt.datetime.utcnow(),
                "autorizado": False,
                "senha": self.hash_password(self.senha_repetir.get_text())
            })
            self.statusbar_login.push(self.statusbar_login.get_context_id('criar_usuario'),
                                      'Solicitação de novo usuário criada. Aguarde aprovação.')
            self.usuario_criado = True
            self.func_cancelar(widget)

    def func_comparar_senhas(self, widget, focus):
        print(widget, focus, self.senha_criar.get_text(), self.senha_repetir.get_text())
        if self.senha_criar.get_text() == self.senha_repetir.get_text():
            self.enviar_solicitacao.set_sensitive(True)
        else:
            self.enviar_solicitacao.set_sensitive(False)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(str(password).encode()).hexdigest()
