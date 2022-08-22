# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('show_refeer/<int:id_refeer>',views.show_refeer,name='show_refeer'),
    path('lectura/<int:id_refeer>/<int:id_sensor>',views.lectura,name="lectura"),
    path('update',views.input_lectura,name="update"),
    path('administrador',views.administrador,name="administrador")
    # Matches any html file
]
