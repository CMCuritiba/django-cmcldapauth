# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch, MagicMock, Mock
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase, RequestFactory

from ..views import loga
from cmcldapauth.lib.msconsumer import MSCMCConsumer, Pessoa, Setor

class AutenticaViewTests(TestCase):
    fixtures = ['autentica.json']

    nome_usuario = 'tora'
    senha = 'mandioca'

    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()

    def consome_pessoa_mock(self, matricula):
        return Pessoa(22, 1111, 'desenv')

    def consome_setor_mock(self, matricula):
        return Setor(11, 'Pinéu', 'PI', 1, True, 'A')


    def test_loga(self):
        request = self.factory.get('/autentica/loga/')
        response = loga(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CMC Autenticação')


    @patch.object(MSCMCConsumer, 'consome_pessoa', consome_pessoa_mock)
    @patch.object(MSCMCConsumer, 'consome_setor', consome_setor_mock)
    def test_valida_usuario(self):
        client = Client()

        response = client.post('/autentica/valida-usuario/', {
            'usuario': 'desenv',
            'senha': 'camara321',
            'next': '/autentica/loga/'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    
    def test_sair(self):
        client = Client()

        response = client.get('/autentica/sair/', follow=True)
        self.assertEqual(response.status_code, 200)