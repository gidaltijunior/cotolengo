import pymongo
from pymongo import errors
import hashlib
import datetime as dt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DefinicoesAplicativo(object):

    def __init__(self, coll_definicoes_aplicativo):

        self.coll_definicoes_aplicativo = coll_definicoes_aplicativo

        builder = Gtk.Builder()
        builder.add_from_file('tela_definicoes_aplicativo.glade')
        self.tela_definicoes_aplicativo = builder.get_object('tela_definicoes_aplicativo')
        self.farmaceutico_responsavel = builder.get_object('farmaceutico_responsavel')
        self.politica_nome_do_farmaceutico_manual = builder.get_object('politica_nome_do_farmaceutico1')
        self.politica_nome_do_farmaceutico_definido = builder.get_object('politica_nome_do_farmaceutico2')
        self.politica_modulos_sem_permissao_desabilitado = builder.get_object('politica_modulos_sem_permissao1')
        self.politica_modulos_sem_permissao_removido = builder.get_object('politica_modulos_sem_permissao2')
        self.politica_acesso_inicial_todos = builder.get_object('politica_acesso_inicial1')
        self.politica_acesso_inicial_nenhum = builder.get_object('politica_acesso_inicial2')
        self.politica_tentativas_conexao = builder.get_object('politica_tentativas_conexao_bd_spin')
        self.salvar_e_fechar = builder.get_object('salvar_e_fechar')
        self.statusbar_definicoes_aplicativo = builder.get_object('statusbar_definicoes_aplicativo')

        builder.connect_signals({'on_salvar_e_fechar_clicked': self.salvar_definicoes_e_fechar})

        self.carregar_definicoes()

        self.statusbar_definicoes_aplicativo.push(
            self.statusbar_definicoes_aplicativo.get_context_id('info'),
            'Alterações nessas propriedades podem causar mudanças visíveis somente se o programa for reiniciado.')

        self.tela_definicoes_aplicativo.show_all()

    def carregar_definicoes(self):
        item = self.coll_definicoes_aplicativo.find_one({'_id': 0})
        farmaceutico_responsavel = item['farmaceutico_responsavel']
        politica_nome_farmaceutico = item['politica_nome_farmaceutico']
        politica_modulos_sem_permissao = item['politica_modulos_sem_permissao']
        politica_acesso_inicial = item['politica_acesso_inicial']
        politica_tentativas_conexao = item['politica_tentativas_conexao']

        self.farmaceutico_responsavel.set_text(farmaceutico_responsavel)

        if politica_nome_farmaceutico == 'definido':
            self.politica_nome_do_farmaceutico_definido.set_active(True)
        elif politica_nome_farmaceutico == 'manual':
            self.politica_nome_do_farmaceutico_manual.set_active(True)

        if politica_modulos_sem_permissao == 'desabilitados':
            self.politica_modulos_sem_permissao_desabilitado.set_active(True)
        elif politica_modulos_sem_permissao == 'removidos':
            self.politica_modulos_sem_permissao_removido.set_active(True)

        if politica_acesso_inicial == 'todos':
            self.politica_acesso_inicial_todos.set_active(True)
        elif politica_acesso_inicial == 'nenhum':
            self.politica_acesso_inicial_nenhum.set_active(True)

        self.politica_tentativas_conexao.set_text(str(politica_tentativas_conexao))

    def salvar_definicoes_e_fechar(self, widget):
        print('salvar_definicoes_e_fechar', widget)

        politica_nome_farmaceutico = None
        politica_modulos_sem_permissao = None
        politica_acesso_inicial = None

        farmaceutico_responsavel = self.farmaceutico_responsavel.get_text()

        if self.politica_nome_do_farmaceutico_definido.get_active():
            politica_nome_farmaceutico = 'definido'
        elif self.politica_nome_do_farmaceutico_manual.get_active():
            politica_nome_farmaceutico = 'manual'

        if self.politica_modulos_sem_permissao_desabilitado.get_active():
            politica_modulos_sem_permissao = 'desabilitados'
        elif self.politica_modulos_sem_permissao_removido.get_active():
            politica_modulos_sem_permissao = 'removidos'

        if self.politica_acesso_inicial_todos.get_active():
            politica_acesso_inicial = 'todos'
        elif self.politica_acesso_inicial_nenhum.get_active():
            politica_acesso_inicial = 'nenhum'

        politica_tentativas_conexao = self.politica_tentativas_conexao.get_text()

        self.coll_definicoes_aplicativo.update_one(
            {'_id': 0},
            {'$set': {'farmaceutico_responsavel': farmaceutico_responsavel,
                      'politica_nome_farmaceutico': politica_nome_farmaceutico,
                      'politica_modulos_sem_permissao': politica_modulos_sem_permissao,
                      'politica_acesso_inicial': politica_acesso_inicial,
                      'politica_tentativas_conexao': int(politica_tentativas_conexao)}}
        )
        self.tela_definicoes_aplicativo.close()
