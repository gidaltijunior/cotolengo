import pymongo
from pymongo import errors
import hashlib
import datetime as dt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class CriarUsuario(object):

    def __init__(self, usuarios_db):
        self.usuario_criado = False
        builder = Gtk.Builder()
        builder.add_from_file('tela_criar_usuario.glade')
        self.tela_criar_usuario = builder.get_object('tela_criar_usuario')
        self.nome_completo = builder.get_object('nome_completo')
        self.nome_usuario = builder.get_object('nome_usuario')
        self.email = builder.get_object('email')
        self.senha_criar = builder.get_object('senha_criar')
        self.senha_repetir = builder.get_object('senha_repetir')
        self.fechar = builder.get_object('fechar')
        self.enviar_solicitacao = builder.get_object('enviar_solicitacao')
        self.statusbar_criar_usuario = builder.get_object('statusbar_criar_usuario')
        self.statusbar_login = builder.get_object('statusbar_login')

        self.usuarios_db = usuarios_db

        builder.connect_signals({"on_fechar_clicked": self.func_fechar,
                                 "on_enviar_solicitacao_clicked": self.func_enviar_solicitacao,
                                 "on_senha_criar_focus_out_event": self.func_comparar_senhas,
                                 "on_senha_repetir_focus_out_event": self.func_comparar_senhas})

        self.enviar_solicitacao.set_sensitive(False)

        self.tela_criar_usuario.show_all()

    def func_fechar(self, widget):
        print('func_fechar', widget)
        self.tela_criar_usuario.close()

    def func_enviar_solicitacao(self, widget):
        print('func_enviar_soliciatacao', widget)
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
            self.statusbar_criar_usuario.push(self.statusbar_criar_usuario.get_context_id('criar_usuario'),
                                              'Solicitação de novo usuário criada. Aguarde aprovação.')
            self.usuario_criado = True
            # self.func_fechar(widget)

    def func_comparar_senhas(self, widget, focus):  # compara se o campo senha e o campo repetir senha tem o mesmo valor
        print(widget, focus)
        if self.senha_criar.get_text() == self.senha_repetir.get_text() \
                and len(str(self.senha_repetir.get_text())) > 3 \
                and len(str(self.nome_usuario.get_text())) > 3 \
                and len(str(self.nome_completo.get_text())) > 3 \
                and len(str(self.email.get_text())) > 3\
                and str(self.email.get_text()).find('@') > 0:
            self.enviar_solicitacao.set_sensitive(True)
        else:
            self.enviar_solicitacao.set_sensitive(False)

    @staticmethod
    def hash_password(password):  # transforma a senha em um longo valor hexadecimal indecifrável
        return hashlib.sha256(str(password).encode()).hexdigest()
