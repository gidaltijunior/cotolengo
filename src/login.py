import pymongo
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from base_module import ModuloBase
from criar_usuario import CriarUsuario
import aux


class Login(object):

    def __init__(self):
        self.validacao_ok = False
        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_login.glade')
        self.tela_login = builder.get_object('tela_login')
        self.grid_login = builder.get_object('grid_login')
        self.usuario = builder.get_object('usuario')
        self.senha = builder.get_object('senha')
        self.logar = builder.get_object('logar')
        self.criar_usuario = builder.get_object('criar_usuario')
        self.statusbar_login = builder.get_object('statusbar_login')

        # Setando o 'tab sequence' da tela. Deve ser feito com o container. Nesse caso: o grid.
        self.grid_login.set_focus_chain([self.usuario, self.senha, self.logar, self.criar_usuario])

        try:
            self.banco_dados, self.coll_usuarios, self.coll_definicoes_aplicativo = self.connect_db()
        except TypeError:
            print('Não foi possível conectar ao banco da dados, as coleções não serão definidas.')

        try:
            self.politica_tentativas_conexao, self.politica_acesso_inicial = self.check_definicoes_aplicativo()
        except TypeError:
            print('As definições do aplicativo não foram obtidas. As políticas não serão definidas.')

        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_criar_usuario_clicked": self.func_criar_usuario,
                                 "on_logar_clicked": self.func_logar})

        self.tela_login.show_all()

    def connect_db(self):
        print('Tentativa de conexão com o banco da dados iniciada.')
        for retries in range(3):
            try:
                client = pymongo.MongoClient('mongodb://localhost')
                db = client.get_database('cotolengo')
                coll_usuarios = db.usuarios
                coll_definicoes_aplicativo = db.definicoes_aplicativo
                client.server_info()

                msg = 'Conexão com banco de dados sucedida!'
                self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'), aux.statusbar_no_user(msg))
                banco_dados = {'client': client, 'db': db}
                return banco_dados, coll_usuarios, coll_definicoes_aplicativo
            except pymongo.errors.AutoReconnect:
                print('Banco de Dados não está disponível. Tentando novamente:', retries)
        else:
            self.logar.set_sensitive(False)
            self.criar_usuario.set_sensitive(False)

            msg = 'Conexão com banco de dados falhou. Verifique.'
            self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'), aux.statusbar_no_user(msg))
            self.tela_login.error_bell()

    def func_criar_usuario(self, widget):
        print('func_criar_usuario', widget)
        tela_criar_usuario = CriarUsuario(usuarios_db=self.coll_usuarios,
                                          definicoes_aplicativo=self.coll_definicoes_aplicativo,
                                          politica_tentativas_conexao=self.politica_tentativas_conexao,
                                          politica_acesso_inicial=self.politica_acesso_inicial)
        print('tela_criar_usuario', tela_criar_usuario)

    def func_logar(self, widget):
        print('func_logar', widget)

        for retries in range(self.politica_tentativas_conexao):
            try:
                item = self.coll_usuarios.find_one({'usuario': str(self.usuario.get_text()).lower()})
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'), aux.statusbar_no_user(msg))
            return

        if item is not None:
            if item['autorizado'] is True:
                new_hash = CriarUsuario.hash_password(self.senha.get_text())
                self.validacao_ok = self.compare_hashes(stored_hash=item['senha'], new_hash=new_hash)
            else:
                msg = 'Usuário não autorizado.'
                self.statusbar_login.push(self.statusbar_login.get_context_id('login'), aux.statusbar_no_user(msg))
                self.tela_login.error_bell()
                return
        else:
            msg = 'Usuário não cadastrado.'
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'), aux.statusbar_no_user(msg))
            self.tela_login.error_bell()
            return

        if self.validacao_ok is True:
            self.tela_login.hide()
            usuario = str(self.usuario.get_text()).lower()
            modulobase = ModuloBase(banco_dados=self.banco_dados,
                                    usuario=usuario,
                                    politica_tentativas_conexao=self.politica_tentativas_conexao,
                                    hspw=new_hash)
            print(modulobase)
        else:
            msg = 'Senha incorreta.'
            self.statusbar_login.push(self.statusbar_login.get_context_id('login'), aux.statusbar_no_user(msg))
            self.tela_login.error_bell()

    @staticmethod
    def compare_hashes(stored_hash, new_hash):
        if stored_hash == new_hash:
            return True
        else:
            return False

    def check_definicoes_aplicativo(self):
        for retries in range(3):
            try:
                quantidade_definicoes = self.coll_definicoes_aplicativo.find().count()
                if quantidade_definicoes == 0:
                    self.coll_definicoes_aplicativo.insert({
                        '_id': 0,
                        'farmaceutico_responsavel': 'indefinido',
                        'politica_nome_farmaceutico': 'definido',
                        'politica_modulos_sem_permissao': 'desabilitados',
                        'politica_acesso_inicial': 'todos',
                        'politica_tentativas_conexao': 3
                    })
                    return 3, 'todos'
                item = self.coll_definicoes_aplicativo.find_one({'_id': 0})
                return item['politica_tentativas_conexao'], item['politica_acesso_inicial']
            except errors.AutoReconnect:
                print('Banco de Dados não está disponível. Tentando novamente:', retries)
            except AttributeError:
                print('As coleções não foram definidas no passo anterior, provável erro de conexão com o banco.')
        else:
            self.logar.set_sensitive(False)
            self.criar_usuario.set_sensitive(False)

            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_login.push(self.statusbar_login.get_context_id('db_status'), aux.statusbar_no_user(msg))
