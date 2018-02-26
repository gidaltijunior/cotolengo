import datetime


def statusbar(usuario, mensagem):

    dia = str(datetime.datetime.today().day)
    mes = str(datetime.datetime.today().month)
    ano = str(datetime.datetime.today().year)

    hora = str(datetime.datetime.now().hour)
    minuto = str(datetime.datetime.now().minute)
    segundo = str(datetime.datetime.now().second)

    nova_mensagem = usuario + ' - ' + dia + '/' + mes + '/' + ano + ' às ' + hora + ':' + minuto + ':' + segundo[:2] +\
        ' - ' + mensagem

    return nova_mensagem


def statusbar_no_user(mensagem):

    nova_mensagem = statusbar(usuario='indefinido', mensagem=mensagem)
    return nova_mensagem
