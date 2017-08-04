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

    url(r'^autentica/', include('autentica.urls')),

3. Run `python manage.py migrate` to create the module models.