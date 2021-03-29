from django.conf import settings
from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
from autentica.models import User as Usuario
import ldap
import base64

class AuthBackend:
  def authenticate(self, request, username=None, password=None):
    try:
      l = ldap.initialize(settings.LDAP_AUTH_URL)
      l.protocol_version = ldap.VERSION3

      # l.simple_bind_s("uid=alexandre.odoni,ou=usuarios,dc=cmc,dc=pr,dc=gov,dc=br","123456")
      l.simple_bind_s("uid={},{}".format(username, settings.LDAP_AUTH_SEARCH_BASE), password)

      # l.simple_bind_s("cn=authproxy,dc=cmc,dc=pr,dc=gov,dc=br","authproxy")
      l.simple_bind_s("cn={},{}".format(settings.LDAP_BIND_USERNAME, settings.LDAP_AUTH_BIND_BASE),settings.LDAP_BIND_PASSWORD)

      # results = l.search_s("ou=usuarios,dc=cmc,dc=pr,dc=gov,dc=br", ldap.SCOPE_SUBTREE, "uid=alexandre.odoni")
      results = l.search_s("{}", ldap.SCOPE_SUBTREE, "uid={}".format(settings.LDAP_AUTH_SEARCH_BASE, username))

      # result_type, result_data = l.result(results, 0)

      uid = results[0][1]['uid'][0].decode('utf-8')
      cpf = results[0][1]['employeeNumber'][0].decode('utf-8')
      email = results[0][1]['mail'][0].decode('utf-8')
      username = results[0][1]['uid'][0].decode('utf-8')
      first_name = results[0][1]['givenName'][0].decode('utf-8')
      last_name = results[0][1]['sn'][0].decode('utf-8')
    except:
      return None

    try:
      user = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
      user = Usuario(username=username)  
      user.uid = uid
      user.cpf = cpf
      user.email = email
      user.username = username
      user.first_name = first_name
      user.last_name = last_name
      # user.password = base64.b64encode(password.encode("utf-8"))
      user.save()
    
    return user

  def get_user(self, user_id):
      try:
          return Usuario.objects.get(pk=user_id)
      except Usuario.DoesNotExist:
          return None