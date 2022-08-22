# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Refeer(models.Model):
    id_refeer = models.AutoField(primary_key=True)
    descripcion = models.CharField(default="sin descripción",max_length=200)    
    activo = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = "refeer"
        verbose_name_plural = "refeers"
        indexes = [
            models.Index(
                fields=[
                    "id_refeer",
                ]
            ),
        ]
    
    def __str__(self):
        return f"refeer  id : {self.id_refeer}"
class Ciclo(models.Model):
    id_ciclo = models.AutoField(primary_key=True)
    subciclos = models.CharField(default="", max_length=590)
    subfechas = models.CharField(default="", max_length=590)
    inicio = models.DateField()
    fin = models.DateField()
    observacion = models.CharField(default="", max_length=590)
    id_refeer = models.ForeignKey(
        Refeer,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
    )
        
class LecturaRefeer(models.Model):
    id_lecturarefeer = models.AutoField(primary_key=True)
    sensor = models.IntegerField(default = 0)
    lectura = models.IntegerField(default=0) 
    created = models.DateTimeField(auto_now_add=True)
    es_tierra = models.BooleanField(default =False) #False aire True tierra
    id_refeer = models.ForeignKey(
        Refeer,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    class Meta:
        managed = True
        db_table = "lecturarefeer"
        verbose_name_plural = "lecturasrefeers"
        indexes = [
            models.Index(
                fields=[
                    "id_lecturarefeer",
                ]
            ),
        ]
    
    def __str__(self):
        return f"lectura  id : {self.id_lecturarefeer}"
    
class Alarma(models.Model):
    id_alarma = models.AutoField(primary_key=True)
    inicio = models.DateField()
    fin = models.DateField()
    aire_tierra = models.IntegerField(default=0)
    treshhold = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    on = models.BooleanField(default=False)
    desc = models.CharField(max_length=200,default="")
    color = models.CharField(max_length=200,default="info")
    id_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    id_refeer = models.ForeignKey(
        Refeer,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    class Meta:
        managed = True
        db_table = "alarma"
        verbose_name_plural = "alarmas"
        indexes = [
            models.Index(
                fields=[
                    "id_alarma",
                ]
            ),
        ]
    
    def __str__(self):
        return f"alarma  id : {self.id_alarma}"
# Create your models here.

class AlarmaContacto(models.Model):
    id_alarmacontacto = models.AutoField(primary_key=True)
    status = models.BooleanField(default=True)
    id_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    
    id_alarma = models.ForeignKey(
        Alarma,
        on_delete=models.CASCADE,
        unique=False,
        null = False,
        blank = False
        )
    
    class Meta:
        managed = True
        db_table = "alarmacontacto"
        verbose_name_plural = "alarmas de contactos"
        indexes = [
            models.Index(
                fields=[
                    "id_alarmacontacto",
                ]
            ),
        ]
    
    def __str__(self):
        return f"alarma contacto  id : {self.id_alarmacontacto}"