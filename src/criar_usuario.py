import pymongo
from pymongo import errors
import hashlib
import datetime as dt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class CriarUsuario(object):

    def __init__(self, usuarios_db, definicoes_aplicativo, politica_tentativas_conexao, politica_acesso_inicial):
        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_criar_usuario.glade')
        self.tela_criar_usuario = builder.get_object('tela_criar_usuario')
        self.grid_criar_usuario = builder.get_object('grid_criar_usuario')
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
        self.definicoes_aplicativo = definicoes_aplicativo
        self.politica_tentativas_conexao = politica_tentativas_conexao
        self.politica_acesso_inicial = politica_acesso_inicial

        # tab sequence:
        self.grid_criar_usuario.set_focus_chain([self.nome_completo, self.nome_usuario, self.email, self.senha_criar,
                                                 self.senha_repetir, self.enviar_solicitacao, self.fechar])

        builder.connect_signals({'on_fechar_clicked': self.func_fechar,
                                 'on_enviar_solicitacao_clicked': self.func_enviar_solicitacao,
                                 'on_nome_completo_key_release_event': self.func_validar_formulario,
                                 'on_nome_usuario_key_release_event': self.func_validar_formulario,
                                 'on_email_key_release_event': self.func_validar_formulario,
                                 'on_senha_criar_key_release_event': self.func_validar_formulario,
                                 'on_senha_repetir_key_release_event': self.func_validar_formulario})

        self.enviar_solicitacao.set_sensitive(False)

        self.tela_criar_usuario.show_all()

    def func_fechar(self, widget):
        print('func_fechar', widget)
        self.tela_criar_usuario.close()

    def func_enviar_solicitacao(self, widget):
        print('func_enviar_solicitacao', widget)
        for retries in range(self.politica_tentativas_conexao):
            try:

                cursor = self.usuarios_db.find({})
                for item in cursor:
                    if item['usuario'] == self.nome_usuario.get_text():
                        self.statusbar_criar_usuario.push(self.statusbar_criar_usuario.get_context_id('criar_usuario'),
                                                          'Nome de usuário já existente. Escolha outro.')
                        self.tela_criar_usuario.error_bell()
                        break
                else:
                    if self.politica_acesso_inicial == 'todos':
                        self.usuarios_db.insert({
                            'usuario': str(self.nome_usuario.get_text()).lower(),
                            'nome': str(self.nome_completo.get_text()).title(),
                            'e-mail': str(self.email.get_text()).lower(),
                            'data_solicitacao': dt.datetime.utcnow(),
                            'autorizado': False,
                            'senha': self.hash_password(password=self.senha_repetir.get_text()),
                            'permissoes':
                                {'nova_analise_prescricao': True,
                                 'abrir_analise_prescricao': True,
                                 'abrir_intervencoes': True,
                                 'abrir_esclarecimentos': True,
                                 'dados_por_lar': True,
                                 'dados_totais': True,
                                 'cadastro_morador': True,
                                 'cadastro_medicamento': True,
                                 'historico_analise_prescricao': True,
                                 'historico_cadastro_morador': True,
                                 'historico_cadastro_medicamento': True,
                                 'historico_opcoes_definicoes': True,
                                 'historico_opcoes_usuario': True,
                                 'historico_gerenciamento_permissoes': True,
                                 'historico_intervencoes': True,
                                 'historico_esclarecimentos': True,
                                 'opcoes_definicoes': True,
                                 'opcoes_meu_usuario': True,
                                 'opcoes_gerenciamento_permissoes': True}
                        })
                    elif self.politica_acesso_inicial == 'nenhum':
                        self.usuarios_db.insert({
                            'usuario': str(self.nome_usuario.get_text()).lower(),
                            'nome': str(self.nome_completo.get_text()).title(),
                            'e-mail': str(self.email.get_text()).lower(),
                            'data_solicitacao': dt.datetime.utcnow(),
                            'autorizado': False,
                            'senha': self.hash_password(password=self.senha_repetir.get_text()),
                            'permissoes':
                                {'nova_analise_prescricao': False,
                                 'abrir_analise_prescricao': False,
                                 'abrir_intervencoes': False,
                                 'abrir_esclarecimentos': False,
                                 'dados_por_lar': False,
                                 'dados_totais': False,
                                 'cadastro_morador': False,
                                 'cadastro_medicamento': False,
                                 'historico_analise_prescricao': False,
                                 'historico_cadastro_morador': False,
                                 'historico_cadastro_medicamento': False,
                                 'historico_opcoes_definicoes': False,
                                 'historico_opcoes_usuario': False,
                                 'historico_gerenciamento_permissoes': False,
                                 'historico_intervencoes': False,
                                 'historico_esclarecimentos': False,
                                 'opcoes_definicoes': False,
                                 'opcoes_meu_usuario': False,
                                 'opcoes_gerenciamento_permissoes': False}
                        })
                    self.statusbar_criar_usuario.push(self.statusbar_criar_usuario.get_context_id('criar_usuario'),
                                                      'Solicitação de novo usuário criada. Aguarde aprovação.')
                    break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_criar_usuario.push(self.statusbar_criar_usuario.get_context_id('conexao_banco'),
                                              'Não foi possível estabelecer uma conexão com o banco de dados.')

    def func_validar_formulario(self, widget, focus):  # valida o formulario para habilitar o botao 'enviar solicitacao'
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
