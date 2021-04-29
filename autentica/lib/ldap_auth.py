from django.conf import settings
from django.contrib.auth.hashers import check_password
from autentica.models import User as Usuario
import ldap
import logging

class AuthBackend:
  def authenticate(self, request, username=None, password=None):
    logger = logging.getLogger(__name__)
    # try:
    l = ldap.initialize(settings.LDAP_AUTH_URL, bytes_mode=False)
    l.protocol_version = ldap.VERSION3

    l.simple_bind_s("uid={},{}".format(username, settings.LDAP_AUTH_SEARCH_BASE), password)

    l.simple_bind_s("cn={},{}".format(settings.LDAP_BIND_USERNAME, settings.LDAP_AUTH_BIND_BASE),settings.LDAP_BIND_PASSWORD)

    results = l.search_s(settings.LDAP_AUTH_SEARCH_BASE, ldap.SCOPE_SUBTREE, "uid={}".format(username))

    logger.info(results)

    # uid = results[0][1]['uid'][0].decode('utf-8')
    # cpf = results[0][1]['employeeNumber'][0].decode('utf-8')
    # email = results[0][1]['mail'][0].decode('utf-8')
    # username = results[0][1]['uid'][0].decode('utf-8')
    # first_name = results[0][1]['givenName'][0].decode('utf-8')
    # last_name = results[0][1]['sn'][0].decode('utf-8')

    uid = results[0][1]['uid'][0]
    cpf = results[0][1]['employeeNumber'][0]
    email = results[0][1]['mail'][0]
    # username = results[0][1]['uid'][0]
    first_name = results[0][1]['givenName'][0]
    last_name = results[0][1]['sn'][0]

    logger.info(uid)
    logger.info(cpf)
    logger.info(email)
    logger.info(first_name)
    logger.info(last_name)

    logger.info(uid.decode())
    logger.info(cpf.decode())
    logger.info(email.decode())
    logger.info(first_name.decode())
    logger.info(last_name.decode())

    # except:
      # return None

    try:
      user = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
      user = Usuario(username=username)  
      user.uid = uid.decode()
      user.cpf = cpf.decode()
      user.email = email.decode()
      user.username = username
      user.first_name = first_name.decode()
      user.last_name = last_name.decode()
      user.save()
    
    return user

  def get_user(self, user_id):
      try:
          return Usuario.objects.get(pk=user_id)
      except Usuario.DoesNotExist:
          return None