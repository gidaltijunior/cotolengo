import datetime as dt
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import aux


class GerenciamentoPermissoes(object):

    def __init__(self, banco_dados, politica_tentativas_conexao, usuario):
        self.banco_dados = banco_dados
        self.politica_tentativas_conexao = politica_tentativas_conexao
        self.usuario = usuario

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

        self.checkbutton_nova_analise_prescricao = builder.get_object('checkbutton_nova_analise_prescricao')
        self.checkbutton_abrir_analise_prescricao = builder.get_object('checkbutton_abrir_analise_prescricao')
        self.checkbutton_abrir_intervencoes = builder.get_object('checkbutton_abrir_intervencoes')
        self.checkbutton_abrir_esclarecimentos = builder.get_object('checkbutton_abrir_esclarecimentos')
        self.checkbutton_dados_por_lar = builder.get_object('checkbutton_dados_por_lar')
        self.checkbutton_dados_totais = builder.get_object('checkbutton_dados_totais')
        self.checkbutton_cadastro_morador = builder.get_object('checkbutton_cadastro_morador')
        self.checkbutton_cadastro_medicamento = builder.get_object('checkbutton_cadastro_medicamento')
        self.checkbutton_opcoes_definicoes = builder.get_object('checkbutton_opcoes_definicoes')
        self.checkbutton_opcoes_meu_usuario = builder.get_object('checkbutton_opcoes_meu_usuario')
        self.checkbutton_historico_analise_prescricao = builder.get_object('checkbutton_historico_analise_prescricao')
        self.checkbutton_historico_cadastro_morador = builder.get_object('checkbutton_historico_cadastro_morador')
        self.checkbutton_historico_cadastro_medicamento = builder.get_object(
            'checkbutton_historico_cadastro_medicamento')
        self.checkbutton_historico_opcoes_definicoes = builder.get_object('checkbutton_historico_opcoes_definicoes')
        self.checkbutton_historico_opcoes_usuario = builder.get_object('checkbutton_historico_opcoes_usuario')
        self.checkbutton_historico_gerenciamento_permissoes = builder.get_object(
            'checkbutton_historico_gerenciamento_permissoes')
        self.checkbutton_historico_intervencoes = builder.get_object('checkbutton_historico_intervencoes')
        self.checkbutton_historico_esclarecimentos = builder.get_object('checkbutton_historico_esclarecimentos')
        self.checkbutton_opcoes_gerenciamento_permissoes = builder.get_object(
            'checkbutton_opcoes_gerenciamento_permissoes')

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

        msg = 'Alterar autorizações e permissões sem autorização é um grave risco de segurança das informações.'
        self.statusbar_gerenciamento_permissoes.push(
            self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

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

                msg = 'O usuário "{0}" foi autorizado com sucesso.'.format(valor)
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

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

                msg = 'O usuário "{0}" foi desautorizado com sucesso.'.format(valor)
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def desautorizado_selecionado(self, widget):
        print('desautorizado_selecionado', widget)
        self.botao_desautorizar.set_sensitive(False)
        self.botao_autorizar.set_sensitive(True)
        self.visao_arvore_autorizados.unselect_all()

    def salvar(self, widget):
        print('salvar', widget)
        selecao = self.lista_usuarios.get_selection()
        modelo, iteracao = selecao.get_selected()
        valor = modelo.get_value(iteracao, 0)

        checkbutton_nova_analise_prescricao = self.checkbutton_nova_analise_prescricao.get_active()
        checkbutton_abrir_analise_prescricao = self.checkbutton_abrir_analise_prescricao.get_active()
        checkbutton_abrir_intervencoes = self.checkbutton_abrir_intervencoes.get_active()
        checkbutton_abrir_esclarecimentos = self.checkbutton_abrir_esclarecimentos.get_active()
        checkbutton_dados_por_lar = self.checkbutton_dados_por_lar.get_active()
        checkbutton_dados_totais = self.checkbutton_dados_totais.get_active()
        checkbutton_cadastro_morador = self.checkbutton_cadastro_morador.get_active()
        checkbutton_cadastro_medicamento = self.checkbutton_cadastro_medicamento.get_active()
        checkbutton_opcoes_definicoes = self.checkbutton_opcoes_definicoes.get_active()
        checkbutton_opcoes_meu_usuario = self.checkbutton_opcoes_meu_usuario.get_active()
        checkbutton_historico_analise_prescricao = self.checkbutton_historico_analise_prescricao.get_active()
        checkbutton_historico_cadastro_morador = self.checkbutton_historico_cadastro_morador.get_active()
        checkbutton_historico_cadastro_medicamento = self.checkbutton_historico_cadastro_medicamento.get_active()
        checkbutton_historico_opcoes_definicoes = self.checkbutton_historico_opcoes_definicoes.get_active()
        checkbutton_historico_opcoes_usuario = self.checkbutton_historico_opcoes_usuario.get_active()
        checkbutton_historico_gerenciamento_permissoes = \
            self.checkbutton_historico_gerenciamento_permissoes.get_active()
        checkbutton_historico_intervencoes = self.checkbutton_historico_intervencoes.get_active()
        checkbutton_historico_esclarecimentos = self.checkbutton_historico_esclarecimentos.get_active()
        checkbutton_opcoes_gerenciamento_permissoes = self.checkbutton_opcoes_gerenciamento_permissoes.get_active()

        for retries in range(self.politica_tentativas_conexao):
            try:
                permissoes = self.coll_usuarios.update_one(
                    {'usuario': valor}, {'$set': {
                        'permissoes.nova_analise_prescricao': checkbutton_nova_analise_prescricao,
                        'permissoes.abrir_analise_prescricao': checkbutton_abrir_analise_prescricao,
                        'permissoes.abrir_intervencoes': checkbutton_abrir_intervencoes,
                        'permissoes.abrir_esclarecimentos': checkbutton_abrir_esclarecimentos,
                        'permissoes.dados_por_lar': checkbutton_dados_por_lar,
                        'permissoes.dados_totais': checkbutton_dados_totais,
                        'permissoes.cadastro_morador': checkbutton_cadastro_morador,
                        'permissoes.cadastro_medicamento': checkbutton_cadastro_medicamento,
                        'permissoes.opcoes_definicoes': checkbutton_opcoes_definicoes,
                        'permissoes.opcoes_meu_usuario': checkbutton_opcoes_meu_usuario,
                        'permissoes.historico_analise_prescricao': checkbutton_historico_analise_prescricao,
                        'permissoes.historico_cadastro_morador': checkbutton_historico_cadastro_morador,
                        'permissoes.historico_cadastro_medicamento': checkbutton_historico_cadastro_medicamento,
                        'permissoes.historico_opcoes_definicoes': checkbutton_historico_opcoes_definicoes,
                        'permissoes.historico_opcoes_usuario': checkbutton_historico_opcoes_usuario,
                        'permissoes.historico_gerenciamento_permissoes': checkbutton_historico_gerenciamento_permissoes,
                        'permissoes.historico_intervencoes': checkbutton_historico_intervencoes,
                        'permissoes.historico_esclarecimentos': checkbutton_historico_esclarecimentos,
                        'permissoes.opcoes_gerenciamento_permissoes': checkbutton_opcoes_gerenciamento_permissoes
                    }
                    })
                print('permissões concedidas', permissoes)

                msg = 'Lista de permissões para o usuário "{0}" atualizada com sucesso.'.format(valor)
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

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
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

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
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

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
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def carregar_checkboxes(self, widget):
        print('carregar_checkboxes', widget)
        selecao = self.lista_usuarios.get_selection()
        modelo, iteracao = selecao.get_selected()
        valor = modelo.get_value(iteracao, 0)
        for retries in range(self.politica_tentativas_conexao):
            try:
                permissoes = self.coll_usuarios.find_one({'usuario': valor}, {'_id': 0, 'permissoes': 1})
                print('desautorizados', permissoes)

                if permissoes['permissoes']['nova_analise_prescricao'] is True:
                    self.checkbutton_nova_analise_prescricao.set_active(True)
                else:
                    self.checkbutton_nova_analise_prescricao.set_active(False)

                if permissoes['permissoes']['abrir_analise_prescricao'] is True:
                    self.checkbutton_abrir_analise_prescricao.set_active(True)
                else:
                    self.checkbutton_abrir_analise_prescricao.set_active(False)

                if permissoes['permissoes']['abrir_intervencoes'] is True:
                    self.checkbutton_abrir_intervencoes.set_active(True)
                else:
                    self.checkbutton_abrir_intervencoes.set_active(False)

                if permissoes['permissoes']['abrir_esclarecimentos'] is True:
                    self.checkbutton_abrir_esclarecimentos.set_active(True)
                else:
                    self.checkbutton_abrir_esclarecimentos.set_active(False)

                if permissoes['permissoes']['dados_por_lar'] is True:
                    self.checkbutton_dados_por_lar.set_active(True)
                else:
                    self.checkbutton_dados_por_lar.set_active(False)

                if permissoes['permissoes']['dados_totais'] is True:
                    self.checkbutton_dados_totais.set_active(True)
                else:
                    self.checkbutton_dados_totais.set_active(False)

                if permissoes['permissoes']['cadastro_morador'] is True:
                    self.checkbutton_cadastro_morador.set_active(True)
                else:
                    self.checkbutton_cadastro_morador.set_active(False)

                if permissoes['permissoes']['cadastro_medicamento'] is True:
                    self.checkbutton_cadastro_medicamento.set_active(True)
                else:
                    self.checkbutton_cadastro_medicamento.set_active(False)

                if permissoes['permissoes']['opcoes_definicoes'] is True:
                    self.checkbutton_opcoes_definicoes.set_active(True)
                else:
                    self.checkbutton_opcoes_definicoes.set_active(False)

                if permissoes['permissoes']['opcoes_meu_usuario'] is True:
                    self.checkbutton_opcoes_meu_usuario.set_active(True)
                else:
                    self.checkbutton_opcoes_meu_usuario.set_active(False)

                if permissoes['permissoes']['historico_analise_prescricao'] is True:
                    self.checkbutton_historico_analise_prescricao.set_active(True)
                else:
                    self.checkbutton_historico_analise_prescricao.set_active(False)

                if permissoes['permissoes']['historico_cadastro_morador'] is True:
                    self.checkbutton_historico_cadastro_morador.set_active(True)
                else:
                    self.checkbutton_historico_cadastro_morador.set_active(False)

                if permissoes['permissoes']['historico_cadastro_medicamento'] is True:
                    self.checkbutton_historico_cadastro_medicamento.set_active(True)
                else:
                    self.checkbutton_historico_cadastro_medicamento.set_active(False)

                if permissoes['permissoes']['historico_opcoes_definicoes'] is True:
                    self.checkbutton_historico_opcoes_definicoes.set_active(True)
                else:
                    self.checkbutton_historico_opcoes_definicoes.set_active(False)

                if permissoes['permissoes']['historico_opcoes_usuario'] is True:
                    self.checkbutton_historico_opcoes_usuario.set_active(True)
                else:
                    self.checkbutton_historico_opcoes_usuario.set_active(False)

                if permissoes['permissoes']['historico_gerenciamento_permissoes'] is True:
                    self.checkbutton_historico_gerenciamento_permissoes.set_active(True)
                else:
                    self.checkbutton_historico_gerenciamento_permissoes.set_active(False)

                if permissoes['permissoes']['historico_intervencoes'] is True:
                    self.checkbutton_historico_intervencoes.set_active(True)
                else:
                    self.checkbutton_historico_intervencoes.set_active(False)

                if permissoes['permissoes']['historico_esclarecimentos'] is True:
                    self.checkbutton_historico_esclarecimentos.set_active(True)
                else:
                    self.checkbutton_historico_esclarecimentos.set_active(False)

                if permissoes['permissoes']['opcoes_gerenciamento_permissoes'] is True:
                    self.checkbutton_opcoes_gerenciamento_permissoes.set_active(True)
                else:
                    self.checkbutton_opcoes_gerenciamento_permissoes.set_active(False)

                msg = 'Lista de permissões para o usuário "{0}" carregado com sucesso.'.format(valor)
                self.statusbar_gerenciamento_permissoes.push(
                    self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_gerenciamento_permissoes.push(
                self.statusbar_gerenciamento_permissoes.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def fechar(self, widget):
        print('fechar', widget)
        self.tela_gerenciamento_permissoes.close()
