import logging
from django.conf import settings
from django.contrib.auth.hashers import check_password
from autentica.models import User as Usuario
from django.contrib.auth import get_user_model
import ldap
import logging

UserModel = get_user_model()
logger = logging.getLogger(__name__)

class AuthBackend:
  def authenticate(self, request, username=None, password=None):
    if not username or not password:
        return None

    username = username.strip().lower()

    try:
      # 🔹 conecta LDAP
      l = ldap.initialize(settings.LDAP_AUTH_URL, bytes_mode=False)
      l.protocol_version = ldap.VERSION3

      # 🔹 bind como usuário (valida senha)
      l.simple_bind_s(
          f"uid={username},{settings.LDAP_AUTH_SEARCH_BASE}",
          password
      )

      # 🔹 bind serviço para buscar atributos
      l.simple_bind_s(
          f"cn={settings.LDAP_BIND_USERNAME},{settings.LDAP_AUTH_BIND_BASE}",
          settings.LDAP_BIND_PASSWORD
      )

      results = l.search_s(
          settings.LDAP_AUTH_SEARCH_BASE,
          ldap.SCOPE_SUBTREE,
          f"uid={username}"
      )

      if not results:
          return None

      attrs = results[0][1]

      uid = attrs['uid'][0].decode()
      cpf = attrs.get('employeeNumber', [b''])[0].decode()
      email = attrs.get('mail', [b''])[0].decode()
      first_name = attrs.get('givenName', [b''])[0].decode()
      last_name = attrs.get('sn', [b''])[0].decode()

      # 🔹 cria ou atualiza usuário Django
      user, _ = UserModel.objects.get_or_create(username=uid)

      user.cpf = cpf
      user.email = email
      user.first_name = first_name
      user.last_name = last_name
      # user.is_active = True
      # user.is_staff = True

      # 🔹 senha local inutilizável (LDAP obrigatório)
      user.set_unusable_password()

      user.save()

      return user

    except ldap.INVALID_CREDENTIALS:
        logger.info("LDAP credenciais inválidas para %s", username)
        return None

    except ldap.LDAPError as e:
        logger.error("Erro LDAP para %s: %s", username, e)
        return None

  def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None