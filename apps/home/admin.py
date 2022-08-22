# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from apps.home.models import Alarma,Refeer,AlarmaContacto,Ciclo
admin.site.register(Refeer)
admin.site.register(Alarma)
admin.site.register(AlarmaContacto)
admin.site.register(Ciclo)
# Register your models here.
