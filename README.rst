===========
CMCLDAPAuth
===========

Validation module that uses LDAP data to validade CMC users.


Quick start
-----------

1. Add "cmcldapauth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'autentica',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^autentica/', include('autentica.urls', namespace='autentica')),

3. Run `python manage.py migrate` to create the module models.

4. Add login restriction 

4.1. In your class based view : 

	class ClassName(CMCLoginRequired, ...):
		or
	class ClassName(CMCAdminLoginRequired, ...):

4.2. In your method :

	@login_required
	def your_method(request):

