from django.conf import settings
from django.contrib.auth.hashers import check_password
from autentica.models import User as Usuario
import ldap
import logging

class AuthBackend:
  def authenticate(self, request, username=None, password=None):
    logger = logging.getLogger(__name__)
    try:
      l = ldap.initialize(settings.LDAP_AUTH_URL, bytes_mode=False)
      l.protocol_version = ldap.VERSION3

      l.simple_bind_s("uid={},{}".format(username, settings.LDAP_AUTH_SEARCH_BASE), password)

      l.simple_bind_s("cn={},{}".format(settings.LDAP_BIND_USERNAME, settings.LDAP_AUTH_BIND_BASE),settings.LDAP_BIND_PASSWORD)

      results = l.search_s(settings.LDAP_AUTH_SEARCH_BASE, ldap.SCOPE_SUBTREE, "uid={}".format(username))

      # logger.info(results)

      uid = results[0][1]['uid'][0].decode()
      cpf = results[0][1]['employeeNumber'][0].decode()
      email = results[0][1]['mail'][0].decode()
      first_name = results[0][1]['givenName'][0].decode()
      last_name = results[0][1]['sn'][0].decode()
    except:
      return None

    try:
      user = Usuario.objects.get(username=username)
      user.cpf = cpf
    except Usuario.DoesNotExist:
      user = Usuario(username=username)  
      user.uid = uid
      user.cpf = cpf
      user.email = email
      user.username = username
      user.first_name = first_name
      user.last_name = last_name
      user.save()

    return user

  def get_user(self, user_id):
      try:
          return Usuario.objects.get(pk=user_id)
      except Usuario.DoesNotExist:
          return None