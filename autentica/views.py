# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login, logout
from .lib.ldap_auth import AuthBackend
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django import forms
from django.db import connection, transaction
from .lib.msconsumer import Pessoa, MSCMCConsumer
import logging

import environ

logger = logging.getLogger(__name__)

def loga(request):
	next = request.GET.get('next')
	context = {'next': next}
	return render(request, 'autentica/login.html', context)

def valida_usuario(request):
	autentica = AuthBackend()
	if request.method == 'POST':
		usuario = request.POST.get('usuario')
		senha = request.POST.get('senha')
		next = request.POST.get('next')
		user = autentica.authenticate(request, username=usuario, password=senha)
		if user is not None:
			if user.is_active:
				login(request, user)
				# try:
				# 	atualiza(user, request)
				# except Exception as e:
				# 	print(e)
				# 	messages.add_message(request, messages.ERROR, "Usuário sem permissão de acesso ao sistema.")
				# 	logout(request)
				# 	return redirect('/autentica/loga/?next=' + next)	
				atualiza(user, request)
				if next != None and next != 'None':
					return HttpResponseRedirect(next)
				return render_to_response('index.html', context_instance=RequestContext(request))
			else:
				messages.add_message(request, messages.ERROR, "Usuário válido mas desabilitado.")
				return redirect('/autentica/loga/?next=' + next)
		else:
			messages.add_message(request, messages.ERROR, "Usuário ou senha incorretos.")
			return redirect('/autentica/loga/?next=' + next) 

def sair(request):
	logout(request)
	return HttpResponseRedirect('/autentica/loga/?next=/')			

# ----------------------------------------------------------------------------------------------------------------
# Atualiza setor do usuario de acordo com servico elotech
# ----------------------------------------------------------------------------------------------------------------
def atualiza(usuario, request):
	logger.info('------------1')
	logger.info(usuario)

	cons = MSCMCConsumer()
	logger.info('------------2')
	funcionario = cons.consome_funcionario_cpf(usuario.cpf)
	logger.info('------------3')
	logger.info(funcionario)

	setor = cons.consome_setor(funcionario.set_id)
	logger.info('------------4')

	request.session['pessoa_nome'] = funcionario.pes_nome
	logger.info('------------5')
	request.session['pessoa_matricula'] = funcionario.matricula
	logger.info('------------6')
	request.session['pessoa_pessoa'] = funcionario.pessoa
	logger.info('------------7')
	request.session['pessoa_cpf'] = funcionario.cpf
	logger.info('------------8')

	request.session['setor_nome'] = setor.set_nome
	logger.info('------------9')
	request.session['setor_id'] = setor.set_id
	logger.info('------------10')
	usuario.lotado=funcionario.set_id
	logger.info('------------11')
	usuario.chefia = verifica_chefia(funcionario.funcao)
	logger.info('------------12')
	usuario.pessoa = funcionario.pessoa
	logger.info('------------13')
	usuario.cpf = funcionario.cpf
	logger.info('------------14')
	usuario.matricula = funcionario.matricula
	logger.info('------------15')
	request.session['pessoa_chefia'] = usuario.chefia
	logger.info('------------16')

	logger.info(usuario.lotado)
	logger.info(usuario.chefia)
	logger.info(usuario.pessoa)
	logger.info(usuario.cpf)
	logger.info(usuario.matricula)
	logger.info('------------17')
	usuario.save()
	logger.info('------------18')

def index(request):
	print('INDEX')

# ----------------------------------------------------------------------------------------------------------------
# Verifica se a pessoa ocupa cargo de chefia pelo nome
# ----------------------------------------------------------------------------------------------------------------
def verifica_chefia(funcao):
	if funcao is None:
		return True
	return False