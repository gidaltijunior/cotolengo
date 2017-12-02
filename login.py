import pymongo
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from base_module import ModuloBase
from criar_usuario import CriarUsuario


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
                new_hash = CriarUsuario.hash_password(self.senha.get_text())
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
            modulobase = ModuloBase()
            print(modulobase)
            # NOVA JANELA VEM AQUI !!!!!!!!!!!!!!!!!!!!!!
        else:
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                      'Senha incorreta.')

    @staticmethod
    def compare_hashes(stored_hash, new_hash):
        if stored_hash == new_hash:
            return True
        else:
            return False
