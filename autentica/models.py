# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.
# Copyright (c) The django-ldapdb project

from __future__ import unicode_literals

from ldapdb.models.fields import (CharField, ImageField, ListField, IntegerField)
import ldapdb.models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Usando o AbstractUser para guardar informações extras do LDAP no model
# -----------------------------------------------------------------------------------------------
class User(AbstractUser):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	lotado = models.CharField(max_length=200, blank=True)
	matricula = models.CharField(max_length=200, blank=True)
	pessoa = models.IntegerField(blank=True, null=True)
	chefia = models.NullBooleanField()

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name