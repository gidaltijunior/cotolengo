import datetime as dt
from bson import objectid
from pymongo import errors
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import aux

class DefinicoesAplicativo(object):

    def __init__(self, banco_dados, politica_tentativas_conexao, usuario, pai):

        self.banco_dados = banco_dados
        self.politica_tentativas_conexao_num = politica_tentativas_conexao
        self.usuario = usuario
        self.pai = pai
        self.timeout = 10
        self.coll_definicoes_aplicativo = self.banco_dados['db'].definicoes_aplicativo
        self.coll_valores_intervencao = self.banco_dados['db'].valores_intervencao
        self.coll_valores_prescritor = self.banco_dados['db'].valores_prescritor
        self.coll_valores_evolucao = self.banco_dados['db'].valores_evolucao
        self.coll_valores_alvo_intervencao = self.banco_dados['db'].valores_alvo_intervencao
        self.coll_valores_ponto_critico = self.banco_dados['db'].valores_ponto_critico
        self.coll_valores_acatamento = self.banco_dados['db'].valores_acatamento

        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_definicoes_aplicativo.glade')
        self.tela_definicoes_aplicativo = builder.get_object('tela_definicoes_aplicativo')
        self.farmaceutico_responsavel = builder.get_object('farmaceutico_responsavel')
        self.politica_nome_do_farmaceutico_manual = builder.get_object('politica_nome_do_farmaceutico1')
        self.politica_nome_do_farmaceutico_definido = builder.get_object('politica_nome_do_farmaceutico2')
        self.politica_modulos_sem_permissao_desabilitado = builder.get_object('politica_modulos_sem_permissao1')
        self.politica_modulos_sem_permissao_removido = builder.get_object('politica_modulos_sem_permissao2')
        self.politica_acesso_inicial_todos = builder.get_object('politica_acesso_inicial1')
        self.politica_acesso_inicial_nenhum = builder.get_object('politica_acesso_inicial2')
        self.politica_tentativas_conexao = builder.get_object('politica_tentativas_conexao_bd_spin')

        self.tela_definicoes_aplicativo.set_transient_for(self.pai)

        self.entrada_intervencao = builder.get_object('entrada_intervencao')
        self.lista_intervencao = builder.get_object('lista_intervencao')
        self.armazenamento_intervencao = builder.get_object('armazenamento_intervencao')
        self.coluna_intervencao = Gtk.TreeViewColumn('Intervenção', Gtk.CellRendererText(), text=0)
        self.coluna_intervencao.set_sort_column_id(0)
        self.lista_intervencao.append_column(self.coluna_intervencao)

        self.entrada_prescritor = builder.get_object('entrada_prescritor')
        self.lista_prescritor = builder.get_object('lista_prescritor')
        self.armazenamento_prescritor = builder.get_object('armazenamento_prescritor')
        self.coluna_prescritor = Gtk.TreeViewColumn('Prescritor', Gtk.CellRendererText(), text=0)
        self.coluna_prescritor.set_sort_column_id(0)
        self.lista_prescritor.append_column(self.coluna_prescritor)

        self.entrada_evolucao = builder.get_object('entrada_evolucao')
        self.lista_evolucao = builder.get_object('lista_evolucao')
        self.armazenamento_evolucao = builder.get_object('armazenamento_evolucao')
        self.coluna_evolucao = Gtk.TreeViewColumn('Evolução', Gtk.CellRendererText(), text=0)
        self.coluna_evolucao.set_sort_column_id(0)
        self.lista_evolucao.append_column(self.coluna_evolucao)

        self.entrada_alvo_intervencao = builder.get_object('entrada_alvo_intervencao')
        self.lista_alvo_intervencao = builder.get_object('lista_alvo_intervencao')
        self.armazenamento_alvo_intervencao = builder.get_object('armazenamento_alvo_intervencao')
        self.coluna_alvo_intervencao = Gtk.TreeViewColumn('Alvo Intervenção', Gtk.CellRendererText(), text=0)
        self.coluna_alvo_intervencao.set_sort_column_id(0)
        self.lista_alvo_intervencao.append_column(self.coluna_alvo_intervencao)

        self.entrada_ponto_critico = builder.get_object('entrada_ponto_critico')
        self.lista_ponto_critico = builder.get_object('lista_ponto_critico')
        self.armazenamento_ponto_critico = builder.get_object('armazenamento_ponto_critico')
        self.coluna_ponto_critico = Gtk.TreeViewColumn('Ponto Crítico', Gtk.CellRendererText(), text=0)
        self.coluna_ponto_critico.set_sort_column_id(0)
        self.lista_ponto_critico.append_column(self.coluna_ponto_critico)

        self.entrada_acatamento = builder.get_object('entrada_acatamento')
        self.lista_acatamento = builder.get_object('lista_acatamento')
        self.armazenamento_acatamento = builder.get_object('armazenamento_acatamento')
        self.coluna_acatamento = Gtk.TreeViewColumn('Acatamento', Gtk.CellRendererText(), text=0)
        self.coluna_acatamento.set_sort_column_id(0)
        self.lista_acatamento.append_column(self.coluna_acatamento)

        self.salvar_e_fechar = builder.get_object('salvar_e_fechar')
        self.statusbar_definicoes_aplicativo = builder.get_object('statusbar_definicoes_aplicativo')

        builder.connect_signals({'on_salvar_e_fechar_clicked': self.salvar_definicoes_e_fechar,
                                 'on_adicionar_intervencao_clicked':
                                     (self.adicionar_valores, self.entrada_intervencao, self.coll_valores_intervencao,
                                      self.armazenamento_intervencao, 'intervenção'),
                                 'on_remover_intervencao_clicked':
                                     (self.remover_valores, self.lista_intervencao, self.coll_valores_intervencao,
                                      self.armazenamento_intervencao, 'intervenção'),
                                 'on_adicionar_prescritor_clicked':
                                     (self.adicionar_valores, self.entrada_prescritor, self.coll_valores_prescritor,
                                      self.armazenamento_prescritor, 'prescritor'),
                                 'on_remover_prescritor_clicked':
                                     (self.remover_valores, self.lista_prescritor, self.coll_valores_prescritor,
                                      self.armazenamento_prescritor, 'prescritor'),
                                 'on_adicionar_evolucao_clicked':
                                     (self.adicionar_valores, self.entrada_evolucao, self.coll_valores_evolucao,
                                      self.armazenamento_evolucao, 'evolução'),
                                 'on_remover_evolucao_clicked':
                                     (self.remover_valores, self.lista_evolucao, self.coll_valores_evolucao,
                                      self.armazenamento_evolucao, 'evolução'),
                                 'on_adicionar_alvo_intervencao_clicked':
                                     (self.adicionar_valores, self.entrada_alvo_intervencao,
                                      self.coll_valores_alvo_intervencao, self.armazenamento_alvo_intervencao,
                                      'alvo da intervenção'),
                                 'on_remover_alvo_intervencao_clicked':
                                     (self.remover_valores, self.lista_alvo_intervencao,
                                      self.coll_valores_alvo_intervencao, self.armazenamento_alvo_intervencao,
                                      'alvo da intervenção'),
                                 'on_adicionar_ponto_critico_clicked':
                                     (self.adicionar_valores, self.entrada_ponto_critico,
                                      self.coll_valores_ponto_critico, self.armazenamento_ponto_critico,
                                      'ponto crítico'),
                                 'on_remover_ponto_critico_clicked':
                                     (self.remover_valores, self.lista_ponto_critico, self.coll_valores_ponto_critico,
                                      self.armazenamento_ponto_critico, 'ponto crítico'),
                                 'on_adicionar_acatamento_clicked':
                                     (self.adicionar_valores, self.entrada_acatamento, self.coll_valores_acatamento,
                                      self.armazenamento_acatamento, 'acatamento'),
                                 'on_remover_acatamento_clicked':
                                     (self.remover_valores, self.lista_acatamento, self.coll_valores_acatamento,
                                      self.armazenamento_acatamento, 'acatamento')
                                 })

        msg = 'Alterações nessas propriedades podem causar mudanças visíveis somente se o programa for reiniciado.'
        self.statusbar_definicoes_aplicativo.push(
            self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))

        self.carregar_definicoes()

        self.tela_definicoes_aplicativo.show_all()

    def carregar_definicoes(self):
        for retries in range(self.politica_tentativas_conexao_num):
            try:

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

                self.carregar_valores(self.armazenamento_intervencao, self.coll_valores_intervencao)
                self.carregar_valores(self.armazenamento_prescritor, self.coll_valores_prescritor)
                self.carregar_valores(self.armazenamento_evolucao, self.coll_valores_evolucao)
                self.carregar_valores(self.armazenamento_alvo_intervencao, self.coll_valores_alvo_intervencao)
                self.carregar_valores(self.armazenamento_ponto_critico, self.coll_valores_ponto_critico)
                self.carregar_valores(self.armazenamento_acatamento, self.coll_valores_acatamento)
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            self.salvar_e_fechar.set_sensitive(False)

            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_definicoes_aplicativo.push(
                self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def carregar_valores(self, armazenamento, colecao):
        for retries in range(self.politica_tentativas_conexao_num):
            try:
                armazenamento.clear()
                valores = colecao.find({})
                for valor in valores:
                    armazenamento.append([valor['valor']])
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_definicoes_aplicativo.push(
                self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def adicionar_valores(self, widget, entrada, colecao, armazenamento, nome_tabela_formatado):
        print('adicionar_valores', nome_tabela_formatado, widget)
        if len(str(entrada.get_text()).strip()) > 0:
            valor = entrada.get_text()
            for retries in range(self.politica_tentativas_conexao_num):
                try:
                    objectid_id = colecao.insert_one({'valor': valor}).inserted_id
                    entrada.set_text('')
                    encontrado = None  # para testar abaixo a adição no banco de dados
                    tentativas = 0
                    while encontrado is None and tentativas < self.timeout:
                        print('executado1')
                        encontrado = colecao.find_one({'_id': objectid.ObjectId(objectid_id)})
                        print('executado2')
                        print(encontrado)
                        time.sleep(1)
                        tentativas += 1
                    self.carregar_valores(armazenamento, colecao)

                    msg = 'O item "{0}" foi adicionado à tabela {1} com sucesso.'.format(valor, nome_tabela_formatado)
                    self.statusbar_definicoes_aplicativo.push(
                        self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))
                    break
                except errors.AutoReconnect:
                    print('Tentando reconectar ao banco de dados.')
            else:
                print('conexão com o banco de dados não foi estabelecida')
                msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
                self.statusbar_definicoes_aplicativo.push(
                    self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))
        else:
            msg = 'O campo de entrada da tabela "{0}" deve ser preenchido antes de ser adicionado à tabela.'.format(
                nome_tabela_formatado)
            self.statusbar_definicoes_aplicativo.push(
                self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def remover_valores(self, widget, lista, colecao, armazenamento, nome_tabela_formatado):
        print('remover_valores', nome_tabela_formatado, widget)
        selecao = lista.get_selection()
        modelo, iteracao = selecao.get_selected()
        if iteracao is not None:
            valor = modelo.get_value(iteracao, 0)
            for retries in range(self.politica_tentativas_conexao_num):
                try:
                    deletados = colecao.delete_one({'valor': valor}).deleted_count
                    tentativas = 0
                    while deletados != 1 and tentativas < self.timeout:
                        time.sleep(1)
                        tentativas += 1
                    self.carregar_valores(armazenamento, colecao)

                    msg = 'O item "{0}" foi removido da tabela "{1}" com sucesso.'.format(valor, nome_tabela_formatado)
                    self.statusbar_definicoes_aplicativo.push(
                        self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))
                    break
                except errors.AutoReconnect:
                    print('Tentando reconectar ao banco de dados.')
            else:
                print('conexão com o banco de dados não foi estabelecida')
                msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
                self.statusbar_definicoes_aplicativo.push(
                    self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))
        else:
            msg = 'Um item da tabela "{0}" deve ser selecionado antes de ser removido.'.format(nome_tabela_formatado)
            self.statusbar_definicoes_aplicativo.push(
                self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))

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

        for retries in range(self.politica_tentativas_conexao_num):
            try:
                self.coll_definicoes_aplicativo.update_one(
                    {'_id': 0},
                    {'$set': {'farmaceutico_responsavel': farmaceutico_responsavel,
                              'politica_nome_farmaceutico': politica_nome_farmaceutico,
                              'politica_modulos_sem_permissao': politica_modulos_sem_permissao,
                              'politica_acesso_inicial': politica_acesso_inicial,
                              'politica_tentativas_conexao': int(politica_tentativas_conexao)}}
                )
                self.tela_definicoes_aplicativo.close()
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_definicoes_aplicativo.push(
                self.statusbar_definicoes_aplicativo.get_context_id('info'), aux.statusbar(self.usuario, msg))
