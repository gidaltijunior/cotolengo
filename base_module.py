from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tela_sobre import Sobre
from definicoes_aplicativo import DefinicoesAplicativo
from meu_usuario import MeuUsuario
from gerenciamento_permissoes import GerenciamentoPermissoes


class ModuloBase(object):

    def __init__(self, banco_dados, usuario, politica_tentativas_conexao, hspw):
        self.banco_dados = banco_dados
        self.usuario = usuario
        self.politica_tentativas_conexao = politica_tentativas_conexao
        self.coll_definicoes_aplicativo = banco_dados['db'].definicoes_aplicativo
        self.hspw = hspw

        builder = Gtk.Builder()
        builder.add_from_file('tela_base.glade')
        self.tela_base = builder.get_object('tela_base')
        self.statusbar_base = builder.get_object('statusbar_base')

        self.nova_analise_prescricao = builder.get_object('nova_analise_prescricao')
        self.abrir_analise_prescricao = builder.get_object('abrir_analise_prescricao')
        self.abrir_intervencoes = builder.get_object('abrir_intervencoes')
        self.abrir_esclarecimentos = builder.get_object('abrir_esclarecimentos')
        self.dados_por_lar = builder.get_object('dados_por_lar')
        self.dados_totais = builder.get_object('dados_totais')
        self.cadastro_morador = builder.get_object('cadastro_morador')
        self.cadastro_medicamento = builder.get_object('cadastro_medicamento')
        self.historico_analise_prescricao = builder.get_object('historico_analise_prescricao')
        self.historico_cadastro_morador = builder.get_object('historico_cadastro_morador')
        self.historico_cadastro_medicamento = builder.get_object('historico_cadastro_medicamento')
        self.historico_opcoes_definicoes = builder.get_object('historico_opcoes_definicoes')
        self.historico_opcoes_usuario = builder.get_object('historico_opcoes_usuario')
        self.historico_gerenciamento_permissoes = builder.get_object('historico_gerenciamento_permissoes')
        self.historico_intervencoes = builder.get_object('historico_intervencoes')
        self.historico_esclarecimentos = builder.get_object('historico_esclarecimentos')
        self.opcoes_definicoes = builder.get_object('opcoes_definicoes')
        self.opcoes_meu_usuario = builder.get_object('opcoes_meu_usuario')
        self.opcoes_gerenciamento_permissoes = builder.get_object('opcoes_gerenciamento_permissoes')

        builder.connect_signals({"gtk_main_quit": Gtk.main_quit,
                                 "on_nova_analise_prescricao_activate": self.func_abrir_tela_nova_analise_prescricao,
                                 "on_abrir_analise_prescricao_activate": self.func_abrir_tela_abrir_analise_prescricao,
                                 "on_abrir_intervencoes_activate": self.func_abrir_tela_abrir_intervencoes,
                                 "on_abrir_esclarecimentos_activate": self.func_abrir_tela_abrir_esclarecimentos,
                                 "on_dados_por_lar_activate": self.func_abrir_tela_dados_por_lar,
                                 "on_dados_totais_activate": self.func_abrir_tela_dados_totais,
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
                                 "on_historico_intervencoes_activate": self.func_abrir_tela_historico_intervencoes,
                                 "on_historico_esclarecimentos_activate":
                                     self.func_abrir_tela_historico_esclarecimentos,
                                 "on_opcoes_definicoes_activate": self.func_abrir_tela_opcoes_definicoes,
                                 "on_opcoes_meu_usuario_activate": self.func_abrir_tela_opcoes_meu_usuario,
                                 "on_opcoes_gerenciamento_permissoes_activate":
                                     self.func_abrir_tela_opcoes_gerenciamento_permissoes,
                                 "on_ajuda_documentacao_activate": self.func_abrir_tela_ajuda_documentacao,
                                 "on_ajuda_sobre_activate": self.func_abrir_tela_sobre})

        self.statusbar_base.push(self.statusbar_base.get_context_id('info'), 'Bem-vindo(a) ' + usuario + '!')

        self.tela_base.show_all()

        self.validar_permissoes()

    def func_analisa_permissoes(self, widget):
        pass

    def func_abrir_tela_nova_analise_prescricao(self, widget):
        pass

    def func_abrir_tela_abrir_analise_prescricao(self, widget):
        pass

    def func_abrir_tela_abrir_intervencoes(self, widget):
        pass

    def func_abrir_tela_abrir_esclarecimentos(self, widget):
        pass

    def func_abrir_tela_dados_por_lar(self, widget):
        pass

    def func_abrir_tela_dados_totais(self, widget):
        pass

    def func_abrir_tela_cadastro_morador(self, widget):
        pass

    def func_abrir_tela_cadastro_medicamento(self, widget):
        pass

    def func_abrir_tela_historico_analise_prescricao(self, widget):
        pass

    def func_abrir_tela_historico_cadastro_morador(self, widget):
        pass

    def func_abrir_tela_historico_cadastro_medicamento(self, widget):
        pass

    def func_abrir_tela_historico_opcoes_definicoes(self, widget):
        pass

    def func_abrir_tela_historico_opcoes_usuario(self, widget):
        pass

    def func_abrir_tela_historico_gerenciamento_permissoes(self, widget):
        pass

    def func_abrir_tela_historico_intervencoes(self, widget):
        pass

    def func_abrir_tela_historico_esclarecimentos(self, widget):
        pass

    def func_abrir_tela_opcoes_definicoes(self, widget):
        tela_definicoes_aplicativo = DefinicoesAplicativo(banco_dados=self.banco_dados,
                                                          politica_tentativas_conexao=self.politica_tentativas_conexao)
        print('tela_definicoes_aplicativo', tela_definicoes_aplicativo, widget)

    def func_abrir_tela_opcoes_meu_usuario(self, widget):
        tela_meu_usuario = MeuUsuario(banco_dados=self.banco_dados,
                                      politica_tentativas_conexao=self.politica_tentativas_conexao,
                                      usuario=self.usuario)
        print('tela_definicoes_aplicativo', tela_meu_usuario, widget)

    def func_abrir_tela_opcoes_gerenciamento_permissoes(self, widget):
        tela_gerenciamento_permissoes = GerenciamentoPermissoes(
            banco_dados=self.banco_dados,
            politica_tentativas_conexao=self.politica_tentativas_conexao)
        print('tela_gerenciamento_permissoes', tela_gerenciamento_permissoes, widget)

    def func_abrir_tela_ajuda_documentacao(self, widget):
        pass

    def func_abrir_tela_sobre(self, widget):
        tela_sobre = Sobre(self.tela_base)
        print('func_abrir_tela_sobre', tela_sobre, widget)

    def validar_permissoes(self):
        for retries in range(self.politica_tentativas_conexao):
            try:
                coll_usuarios = self.banco_dados['db'].usuarios
                item = self.coll_definicoes_aplicativo.find_one({'_id': 0})
                politica_modulos_sem_permissao = item['politica_modulos_sem_permissao']

                usuario = coll_usuarios.find_one({'usuario': self.usuario})

                if politica_modulos_sem_permissao == 'desabilitados':
                    if usuario['permissoes']['nova_analise_prescricao'] is False:
                        self.nova_analise_prescricao.set_sensitive(False)
                    if usuario['permissoes']['abrir_analise_prescricao'] is False:
                        self.abrir_analise_prescricao.set_sensitive(False)
                    if usuario['permissoes']['abrir_intervencoes'] is False:
                        self.abrir_intervencoes.set_sensitive(False)
                    if usuario['permissoes']['abrir_esclarecimentos'] is False:
                        self.abrir_esclarecimentos.set_sensitive(False)
                    if usuario['permissoes']['dados_por_lar'] is False:
                        self.dados_por_lar.set_sensitive(False)
                    if usuario['permissoes']['dados_totais'] is False:
                        self.dados_totais.set_sensitive(False)
                    if usuario['permissoes']['cadastro_morador'] is False:
                        self.cadastro_morador.set_sensitive(False)
                    if usuario['permissoes']['cadastro_medicamento'] is False:
                        self.cadastro_medicamento.set_sensitive(False)
                    if usuario['permissoes']['historico_analise_prescricao'] is False:
                        self.historico_analise_prescricao.set_sensitive(False)
                    if usuario['permissoes']['historico_cadastro_morador'] is False:
                        self.historico_cadastro_morador.set_sensitive(False)
                    if usuario['permissoes']['historico_cadastro_medicamento'] is False:
                        self.historico_cadastro_medicamento.set_sensitive(False)
                    if usuario['permissoes']['historico_opcoes_definicoes'] is False:
                        self.historico_opcoes_definicoes.set_sensitive(False)
                    if usuario['permissoes']['historico_opcoes_usuario'] is False:
                        self.historico_opcoes_usuario.set_sensitive(False)
                    if usuario['permissoes']['historico_gerenciamento_permissoes'] is False:
                        self.historico_gerenciamento_permissoes.set_sensitive(False)
                    if usuario['permissoes']['historico_intervencoes'] is False:
                        self.historico_intervencoes.set_sensitive(False)
                    if usuario['permissoes']['historico_esclarecimentos'] is False:
                        self.historico_esclarecimentos.set_sensitive(False)
                    if usuario['permissoes']['opcoes_definicoes'] is False:
                        self.opcoes_definicoes.set_sensitive(False)
                    if usuario['permissoes']['opcoes_meu_usuario'] is False:
                        self.opcoes_meu_usuario.set_sensitive(False)
                    if usuario['permissoes']['opcoes_gerenciamento_permissoes'] is False:
                        self.opcoes_gerenciamento_permissoes.set_sensitive(False)

                elif politica_modulos_sem_permissao == 'removidos':
                    if usuario['permissoes']['nova_analise_prescricao'] is False:
                        self.nova_analise_prescricao.hide()
                    if usuario['permissoes']['abrir_analise_prescricao'] is False:
                        self.abrir_analise_prescricao.hide()
                    if usuario['permissoes']['abrir_intervencoes'] is False:
                        self.abrir_intervencoes.hide()
                    if usuario['permissoes']['abrir_esclarecimentos'] is False:
                        self.abrir_esclarecimentos.hide()
                    if usuario['permissoes']['dados_por_lar'] is False:
                        self.dados_por_lar.hide()
                    if usuario['permissoes']['dados_totais'] is False:
                        self.dados_totais.hide()
                    if usuario['permissoes']['cadastro_morador'] is False:
                        self.cadastro_morador.hide()
                    if usuario['permissoes']['cadastro_medicamento'] is False:
                        self.cadastro_medicamento.hide()
                    if usuario['permissoes']['historico_analise_prescricao'] is False:
                        self.historico_analise_prescricao.hide()
                    if usuario['permissoes']['historico_cadastro_morador'] is False:
                        self.historico_cadastro_morador.hide()
                    if usuario['permissoes']['historico_cadastro_medicamento'] is False:
                        self.historico_cadastro_medicamento.hide()
                    if usuario['permissoes']['historico_opcoes_definicoes'] is False:
                        self.historico_opcoes_definicoes.hide()
                    if usuario['permissoes']['historico_opcoes_usuario'] is False:
                        self.historico_opcoes_usuario.hide()
                    if usuario['permissoes']['historico_gerenciamento_permissoes'] is False:
                        self.historico_gerenciamento_permissoes.hide()
                    if usuario['permissoes']['historico_intervencoes'] is False:
                        self.historico_intervencoes.hide()
                    if usuario['permissoes']['historico_esclarecimentos'] is False:
                        self.historico_esclarecimentos.hide()
                    if usuario['permissoes']['opcoes_definicoes'] is False:
                        self.opcoes_definicoes.hide()
                    if usuario['permissoes']['opcoes_meu_usuario'] is False:
                        self.opcoes_meu_usuario.hide()
                    if usuario['permissoes']['opcoes_gerenciamento_permissoes'] is False:
                        self.opcoes_gerenciamento_permissoes.hide()

                else:
                    self.nova_analise_prescricao.hide()
                    self.abrir_analise_prescricao.hide()
                    self.abrir_intervencoes.hide()
                    self.abrir_esclarecimentos.hide()
                    self.dados_por_lar.hide()
                    self.dados_totais.hide()
                    self.cadastro_morador.hide()
                    self.cadastro_medicamento.hide()
                    self.historico_analise_prescricao.hide()
                    self.historico_cadastro_morador.hide()
                    self.historico_cadastro_medicamento.hide()
                    self.historico_opcoes_definicoes.hide()
                    self.historico_opcoes_usuario.hide()
                    self.historico_gerenciamento_permissoes.hide()
                    self.historico_intervencoes.hide()
                    self.historico_esclarecimentos.hide()
                    self.opcoes_definicoes.hide()
                    self.opcoes_meu_usuario.hide()
                    self.opcoes_gerenciamento_permissoes.hide()
                    self.statusbar_base.push(self.statusbar_base.get_context_id('permissoes'),
                                             'Não foi possível acessar as políticas de módulos sem permissão.')
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.statusbar_base.push(self.statusbar_base.get_context_id('db_status'),
                                     'Não foi possível estabelecer uma conexão com o banco de dados.')
