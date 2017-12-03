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

        self.banco_dados, self.coll_usuarios, self.coll_definicoes_aplicativo = self.connect_db()

        self.check_definicoes_aplicativo()

        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_criar_usuario_clicked": self.func_criar_usuario,
                                 "on_logar_clicked": self.func_logar})

        self.tela_login.show_all()

    def connect_db(self):
        print('connect db')
        client, db, coll_usuarios, coll_definicoes_aplicativo = None, None, None, None
        for retries in range(3):
            try:
                client = pymongo.MongoClient('mongodb://localhost')
                db = client.get_database('cotolengo')
                coll_usuarios = db.usuarios
                coll_definicoes_aplicativo = db.definicoes_aplicativo
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
                self.tela_login.error_bell()
        banco_dados = {'client': client, 'db': db}
        return banco_dados, coll_usuarios, coll_definicoes_aplicativo

    def func_criar_usuario(self, widget):
        print('func_criar_usuario', widget)
        tela_criar_usuario = CriarUsuario(usuarios_db=self.coll_usuarios,
                                          definicoes_aplicativo=self.coll_definicoes_aplicativo)
        print('tela_criar_usuario', tela_criar_usuario)

    def func_logar(self, widget):
        print('func_logar', widget)
        item = self.coll_usuarios.find_one({'usuario': str(self.usuario.get_text()).lower()})
        if item is not None:
            if item['autorizado'] is True:
                new_hash = CriarUsuario.hash_password(self.senha.get_text())
                self.validacao_ok = self.compare_hashes(stored_hash=item['senha'], new_hash=new_hash)
            else:
                self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                          'Usuário não autorizado.')
                self.tela_login.error_bell()
                return
        else:
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                      'Usuário não cadastrado.')
            self.tela_login.error_bell()
            return

        if self.validacao_ok is True:
            self.tela_login.hide()
            usuario = str(self.usuario.get_text()).lower()
            modulobase = ModuloBase(banco_dados=self.banco_dados, usuario=usuario)
            print(modulobase)
        else:
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'),
                                      'Senha incorreta.')
            self.tela_login.error_bell()

    @staticmethod
    def compare_hashes(stored_hash, new_hash):
        if stored_hash == new_hash:
            return True
        else:
            return False

    def check_definicoes_aplicativo(self):
        quantidade_definicoes = self.coll_definicoes_aplicativo.find().count()
        if quantidade_definicoes == 0:
            self.coll_definicoes_aplicativo.insert({
                'farmaceutico_responsavel': 'indefinido',
                'politica_nome_farmaceutico': 'definido',
                'politica_modulos_sem_permissao': 'desabilitados',
                'politica_acesso_inicial': 'todos',
                'politica_tentativas_conexao': 3
            })
