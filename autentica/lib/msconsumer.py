import environ
import simplejson as json
from django.conf import settings

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Pessoa(object):
	def __init__(self, set_id, pes_matricula, pes_nome):	
		self.set_id = set_id
		self.pes_matricula = pes_matricula
		self.pes_nome = pes_nome

class Setor(object):
	def __init__(self, set_id, set_nome, set_sigla, set_id_superior, set_ativo, set_tipo):	
		self.set_id = set_id
		self.set_nome = set_nome
		self.set_sigla = set_sigla
		self.set_id_superior = set_id_superior
		self.set_ativo = set_ativo
		self.set_tipo = set_tipo

class Funcionario(object):
	def __init__(self, matricula, pessoa, pes_nome, funcao, set_id, ind_estagiario):	
		self.matricula = matricula
		self.pessoa = pessoa
		self.pes_nome = pes_nome		
		self.funcao = funcao
		self.set_id = set_id
		self.ind_estagiario = ind_estagiario

# ----------------------------------------------------------------------------------------------------------------
# Classe responsável por consumir as informações JSON 
# ----------------------------------------------------------------------------------------------------------------
class MSCMCConsumer(object):

	def __init__(self):
		self.MSCMC_SERVER = settings.MSCMC_SERVER

	# ----------------------------------------------------------------------------------------------------------------
	# Consome o serviço que retorna dados da pessoa através da matrícula
	# ----------------------------------------------------------------------------------------------------------------
	def consome_pessoa(self, matricula):
		search_url = '{}/api/pessoa/{}/?format=json'.format(self.MSCMC_SERVER, matricula)
		print('----------------1')
		r = requests.get(search_url, verify=False)
		print('----------------2')
		js = r.json()
		print('----------------3')
		return Pessoa(js['set_id'], js['pes_matricula'], js['pes_nome'])

	# ----------------------------------------------------------------------------------------------------------------
	# Consome o serviço que retorna dados da pessoa através da matrícula
	# ----------------------------------------------------------------------------------------------------------------
	def consome_setor(self, set_id):
		search_url = '{}/api/setor_setor/{}/?format=json'.format(self.MSCMC_SERVER, set_id)
		print('----------------4')
		r = requests.get(search_url, verify=False)
		print('----------------5')
		js = r.json()
		print('----------------6')
		return Setor(js['set_id'], js['set_nome'], js['set_sigla'], js['set_id_superior'], js['set_ativo'], js['set_tipo'])

	# ----------------------------------------------------------------------------------------------------------------
	# Consome o serviço que retorna dados do funcionario através da chave
	# ----------------------------------------------------------------------------------------------------------------
	def consome_funcionario(self, chave):
		search_url = '{}/api/funcionario/{}/?format=json'.format(self.MSCMC_SERVER, chave)
		print('----------------7')
		r = requests.get(search_url, verify=False)
		print('----------------8')
		js = r.json()
		print('----------------9')
		return Funcionario(js['matricula'], js['pessoa'], js['pes_nome'], js['funcao'], js['set_id'], js['ind_estagiario'])		

		