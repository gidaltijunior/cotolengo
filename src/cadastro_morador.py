import time
import datetime as dt
import pymongo
from bson.objectid import ObjectId
from pymongo import errors
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import aux


class CadastroMorador(object):

    def __init__(self, usuario, banco_dados, politica_tentativas_conexao):

        self.usuario = usuario
        self.banco_dados = banco_dados
        self.politica_tentativas_conexao = politica_tentativas_conexao
        self.coll_moradores = self.banco_dados['db'].moradores
        self.timeout = 10

        builder = Gtk.Builder()
        builder.add_from_file('glade/tela_cadastro_morador.glade')

        self.tela_cadastro_morador = builder.get_object('tela_cadastro_morador')

        self.lista_moradores = builder.get_object('lista_moradores')
        self.armazenamento_moradores = builder.get_object('armazenamento_moradores')
        self.coluna_objectid = Gtk.TreeViewColumn('ObjectID', Gtk.CellRendererText(), text=0)
        self.coluna_nome = Gtk.TreeViewColumn('Nome', Gtk.CellRendererText(), text=1)
        self.coluna_data_nascimento = Gtk.TreeViewColumn('Data Nascimento', Gtk.CellRendererText(), text=2)
        self.coluna_sexo = Gtk.TreeViewColumn('Sexo', Gtk.CellRendererText(), text=3)
        self.coluna_lar = Gtk.TreeViewColumn('Lar', Gtk.CellRendererText(), text=4)
        self.coluna_peso = Gtk.TreeViewColumn('Peso', Gtk.CellRendererText(), text=5)
        self.coluna_ativo = Gtk.TreeViewColumn('Ativo', Gtk.CellRendererText(), text=6)

        self.coluna_nome.set_sort_column_id(1)
        self.coluna_nome.set_resizable(True)
        self.coluna_data_nascimento.set_sort_column_id(2)
        self.coluna_data_nascimento.set_resizable(True)
        self.coluna_sexo.set_sort_column_id(3)
        self.coluna_sexo.set_resizable(True)
        self.coluna_lar.set_sort_column_id(4)
        self.coluna_lar.set_resizable(True)
        self.coluna_peso.set_sort_column_id(5)
        self.coluna_peso.set_resizable(True)
        self.coluna_ativo.set_sort_column_id(6)
        self.coluna_ativo.set_resizable(True)

        # self.lista_moradores.append_column(self.coluna_objectid)
        self.lista_moradores.append_column(self.coluna_nome)
        self.lista_moradores.append_column(self.coluna_data_nascimento)
        self.lista_moradores.append_column(self.coluna_sexo)
        self.lista_moradores.append_column(self.coluna_lar)
        self.lista_moradores.append_column(self.coluna_peso)
        self.lista_moradores.append_column(self.coluna_ativo)

        self.atualizar_nome = builder.get_object('atualizar_nome')
        self.atualizar_nascimento = builder.get_object('atualizar_nascimento')
        self.atualizar_calendario = builder.get_object('atualizar_calendario')
        self.atualizar_feminino = builder.get_object('atualizar_feminino')
        self.atualizar_masculino = builder.get_object('atualizar_masculino')
        self.atualizar_lar = builder.get_object('atualizar_lar')
        self.atualizar_peso = builder.get_object('atualizar_peso')
        self.atualizar_observacoes = builder.get_object('atualizar_observacoes')
        self.atualizar_textbuffer = builder.get_object('atualizar_textbuffer')
        self.atualizar_ativo = builder.get_object('atualizar_ativo')
        self.atualizar = builder.get_object('atualizar')

        self.novo_nome = builder.get_object('novo_nome')
        self.novo_data_nascimento = builder.get_object('novo_data_nascimento')
        self.novo_calendario = builder.get_object('novo_calendario')
        self.novo_feminino = builder.get_object('novo_feminino')
        self.novo_masculino = builder.get_object('novo_masculino')
        self.novo_lar = builder.get_object('novo_lar')
        self.novo_peso = builder.get_object('novo_peso')
        self.novo_observacoes = builder.get_object('novo_observacoes')
        self.novo_textbuffer = builder.get_object('novo_textbuffer')
        self.adicionar = builder.get_object('adicionar')

        self.statusbar_cadastro_moradores = builder.get_object('statusbar_cadastro_moradores')

        builder.connect_signals({'on_atualizar_clicked': self.atualizar_dados,
                                 'on_list_moradores_cursor_changed': self.detalhar_dados,
                                 'on_atualizar_nascimento_focus_out_event': (
                                     self.corrigir_calendario, self.atualizar_nascimento, self.atualizar_calendario),
                                 'on_atualizar_calendario_day_selected': (
                                     self.corrigir_nascimento, self.atualizar_nascimento, self.atualizar_calendario),
                                 'on_adicionar_clicked': self.incluir_morador,
                                 'on_novo_data_nascimento_focus_out_event': (
                                         self.corrigir_calendario, self.novo_data_nascimento, self.novo_calendario),
                                 'on_novo_calendario_day_selected': (
                                     self.corrigir_nascimento, self.novo_data_nascimento, self.novo_calendario),
                                 'on_fechar_clicked': self.fechar
                                 })

        self.carregar_lista()

        self.tela_cadastro_morador.show_all()

    def carregar_lista(self):
        print('carregar_lista')
        for retries in range(self.politica_tentativas_conexao):
            try:
                self.armazenamento_moradores.clear()
                valores = self.coll_moradores.find().sort('nome', pymongo.ASCENDING)
                for valor in valores:
                    valor['data_nascimento'] = str('{:%d/%m/%Y}').format(valor['data_nascimento'])
                    valor['peso'] = str('{:0>5.5} Kgs').format(valor['peso'])
                    if valor['ativo'] is True:
                        valor['ativo'] = 'Sim'
                    else:
                        valor['ativo'] = 'Não'

                    self.armazenamento_moradores.append(
                        [str(valor['_id']),
                         valor['nome'],
                         valor['data_nascimento'],
                         valor['sexo'],
                         valor['lar'],
                         valor['peso'],
                         valor['ativo']
                         ])
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def detalhar_dados(self, widget):
        print('detalhar_dados', widget)

        try:
            selecao = self.lista_moradores.get_selection()
            modelo, iteracao = selecao.get_selected()
            obj_id = modelo.get_value(iteracao, 0)
        except TypeError:
            return

        for retries in range(self.politica_tentativas_conexao):
            try:
                morador = self.coll_moradores.find_one({'_id': ObjectId(obj_id)})
                print('morador', morador)

                self.atualizar_nome.set_text(morador['nome'])
                data_nascimento = str('{:%d/%m/%Y}').format(morador['data_nascimento'])
                self.atualizar_nascimento.set_text(data_nascimento)

                self.atualizar_calendario.select_month(int(data_nascimento[3:5]) - 1,
                                                       int(data_nascimento[6:]))
                self.atualizar_calendario.select_day(int(data_nascimento[:2]))

                if morador['sexo'] == 'F':
                    self.atualizar_feminino.set_active(True)
                else:
                    self.atualizar_masculino.set_active(True)

                self.atualizar_lar.set_text(morador['lar'])

                peso = str('{:>7.6}').format(morador['peso']).replace('.', ',')
                self.atualizar_peso.set_text(peso)

                self.atualizar_textbuffer.set_text(morador['observacoes'], -1)

                if morador['ativo'] is True:
                    self.atualizar_ativo.set_active(True)
                else:
                    self.atualizar_ativo.set_active(False)

                msg = 'Detalhes do morador "{0}" carregado com sucesso.'.format(morador['nome'])
                self.statusbar_cadastro_moradores.push(
                    self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))

    def atualizar_dados(self, widget):
        print('atualizar_dados', widget)

        selecao = self.lista_moradores.get_selection()
        modelo, iteracao = selecao.get_selected()
        obj_id = modelo.get_value(iteracao, 0)

        nome = self.atualizar_nome.get_text()
        nascimento = self.atualizar_nascimento.get_text()
        lar = self.atualizar_lar.get_text()
        peso = self.atualizar_peso.get_text()
        observacoes = self.atualizar_textbuffer.get_text(
            self.atualizar_textbuffer.get_start_iter(), self.atualizar_textbuffer.get_end_iter(), True)
        ativo = self.atualizar_ativo.get_active()

        if self.atualizar_feminino.get_active():
            sexo = 'F'
        else:
            sexo = 'M'

        if len(nome) > 0:
            pass
        else:
            msg = 'Campo "Nome" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        if len(nascimento) > 9:
            try:
                nascimento = dt.datetime(int(nascimento[6:]), int(nascimento[3:5]), int(nascimento[0:2]), 0, 0, 0, 0,
                                         tzinfo=dt.timezone.utc)
            except Exception as e:
                print(Exception, e)
                msg = 'Conteúdo do campo "Data de Nascimento" não é valido. Formato esperado é DD/MM/AAAA.'
                self.statusbar_cadastro_moradores.push(
                    self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
                self.tela_cadastro_morador.error_bell()
                return
        else:
            msg = 'Campo "Data de Nascimento" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        if len(lar) > 0:
            pass
        else:
            msg = 'Campo "Lar" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        peso = str(peso).replace(',', '.')

        if float(peso) > 0:
            peso = float(peso)
        else:
            msg = 'Campo "Peso" não pode ser zero.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        for retries in range(self.politica_tentativas_conexao):
            try:
                objectid_id = self.coll_moradores.update_one(
                    {'_id': ObjectId(obj_id)},
                    {'$set': {'nome': nome,
                              'data_nascimento': nascimento,
                              'sexo': sexo,
                              'lar': lar,
                              'peso': peso,
                              'observacoes': observacoes,
                              'ativo': ativo}
                     }
                )
                print('Atualização realizada para object_id:', objectid_id)

                path = modelo.get_path(iteracao)  # o número da linha na lista de moradores
                self.carregar_lista()  # refresh na lista de moradores
                self.lista_moradores.set_cursor(path)  # selecionamos a mesma linha antes do refresh

                msg = 'O cadastro do morador "{0}" foi atualizado com sucesso.'.format(nome)
                self.statusbar_cadastro_moradores.push(
                    self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            print('conexão com o banco de dados não foi estabelecida')
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()

    def incluir_morador(self, widget):
        print('incluir_morador', widget)

        nome = self.novo_nome.get_text()
        nascimento = self.novo_data_nascimento.get_text()
        lar = self.novo_lar.get_text()
        peso = self.novo_peso.get_text()
        observacoes = self.novo_textbuffer.get_text(
            self.novo_textbuffer.get_start_iter(), self.novo_textbuffer.get_end_iter(), True)
        ativo = True

        if self.novo_feminino.get_active():
            sexo = 'F'
        else:
            sexo = 'M'

        if len(nome) > 0:
            pass
        else:
            msg = 'Campo "Nome" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        if len(nascimento) > 9:
            try:
                nascimento = dt.datetime(int(nascimento[6:]), int(nascimento[3:5]), int(nascimento[0:2]), 0, 0, 0, 0,
                                         tzinfo=dt.timezone.utc)
            except Exception as e:
                print(Exception, e)
                msg = 'Conteúdo do campo "Data de Nascimento" não é valido. Formato esperado é DD/MM/AAAA.'
                self.statusbar_cadastro_moradores.push(
                    self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
                self.tela_cadastro_morador.error_bell()
                return
        else:
            msg = 'Campo "Data de Nascimento" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        if len(lar) > 0:
            pass
        else:
            msg = 'Campo "Lar" não pode estar vazio.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        peso = str(peso).replace(',', '.')

        if float(peso) > 0:
            peso = float(peso)
        else:
            msg = 'Campo "Peso" não pode ser zero.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

        for retries in range(self.politica_tentativas_conexao):
            try:
                objectid_id = self.coll_moradores.insert_one(
                    {
                        'nome': nome,
                        'data_nascimento': nascimento,
                        'sexo': sexo,
                        'lar': lar,
                        'peso': peso,
                        'observacoes': observacoes,
                        'ativo': ativo
                    }
                ).inserted_id

                encontrado = None  # para testar abaixo a adição no banco de dados
                tentativas = 0
                while encontrado is None and tentativas < self.timeout:
                    print('executado1')
                    encontrado = self.coll_moradores.find_one({'_id': ObjectId(objectid_id)})
                    print('executado2')
                    print(encontrado)
                    time.sleep(1)
                    tentativas += 1
                self.carregar_lista()
                self.novo_nome.set_text('')
                self.novo_data_nascimento.set_text('')
                self.novo_lar.set_text('')
                self.novo_peso.set_text('')
                self.novo_textbuffer.set_text('', -1)

                msg = 'O morador \'{0}\' foi adicionado ao cadastro com sucesso.'.format(nome)
                self.statusbar_cadastro_moradores.push(
                    self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
                break
            except errors.AutoReconnect:
                print('Tentando reconectar ao banco de dados.')
        else:
            msg = 'Não foi possível estabelecer uma conexão com o banco de dados.'
            print('conexão com o banco de dados não foi estabelecida')
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()

    def corrigir_calendario(self, widget, focus, campo_data, calendario):
        print('corrigir_calendatio', widget, focus, campo_data, calendario)
        data = campo_data.get_text()
        try:
            calendario.select_month(int(data[3:5]) - 1, int(data[6:]))
            calendario.select_day(int(data[:2]))
        except Exception as e:
            print(type(e), e)
            msg = 'Conteúdo do campo "Data de Nascimento" não é valido. Formato esperado é DD/MM/AAAA.'
            self.statusbar_cadastro_moradores.push(
                self.statusbar_cadastro_moradores.get_context_id('info'), aux.statusbar(self.usuario, msg))
            self.tela_cadastro_morador.error_bell()
            return

    @staticmethod
    def corrigir_nascimento(widget, campo_data, calendario):
        print('corrigir_nascimento', widget, campo_data, calendario)
        data = calendario.get_date()
        campo_data.set_text(str(data[2]).zfill(2) + '/' + str((data[1]+1)).zfill(2) + '/' + str(data[0]))

    def fechar(self, widget):
        print('fechar', widget)
        self.tela_cadastro_morador.close()
