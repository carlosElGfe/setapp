# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *
import numpy as np
from stl import mesh
import io
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import proj3d
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import random
import datetime
from .utils import *
from django.contrib.auth.models import User
def ger_refeer():
    figure = Figure()
    axes = mplot3d.Axes3D(figure)
    # Define the 8 vertices of the cube
    vertices = np.array([\
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1],
        [-1, -1, +1],
        [+1, -1, +1],
        [+1, +1, +1],
        [-1, +1, +1]])
    # Define the 12 triangles composing the cube
    faces = np.array([\
        [0,3,1],
        [1,3,2],
        [0,4,7],
        [0,7,3],
        [4,5,6],
        [4,6,7],
        [5,1,2],
        [5,2,6],
        [2,3,6],
        [3,7,6],
        [0,1,5],
        [0,5,4]])

    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]
    your_mesh = cube
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    output = io.BytesIO()
    canvas = FigureCanvas(figure)
    canvas.print_png(output)
    img_str = base64.b64encode(output.getvalue())
    data_url = 'data:image/jpg;base64,' + base64.b64encode(output.getvalue()).decode()
    return data_url

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['fecha_actual'] = get_fecha_actual()
    context['alarmas'] = get_my_homework()
    print(context['alarmas'])
    context['image']=ger_refeer()
    context['refeers'] = Refeer.objects.all()
    context['ac'] = AlarmaContacto.objects.filter(id_user=request.user).all()
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def show_refeer(request,id_refeer):
    context = {'segment': 'index'}
    refeer = Refeer.objects.filter(id_refeer=id_refeer).first()
    context['lectura_1'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 1).order_by("-created").first().lectura
    context['lectura_2'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 2).order_by("-created").first().lectura
    context['lectura_3'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 3).order_by("-created").first().lectura
    context['lectura_4'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 4).order_by("-created").first().lectura
    context['lectura_5'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 5).order_by("-created").first().lectura
    context['lectura_6'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 6).order_by("-created").first().lectura
    get_last_lecturas_refeer(refeer,context,8)
    context['lec_1'] = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 1).order_by("-created")[:5]
    print(context['lec_1'])
    context['last_20_lectures'] = LecturaRefeer.objects.filter(id_refeer = refeer).order_by("-created")[:20]
    context['refeer'] = refeer
    if request.method == 'POST':
        if request.POST.get("alarma"):
            print(request.POST.get("fecha_alarma"))
            fecha_i = request.POST.get("fecha_alarma").split(" ")[0] 
            fecha_f = request.POST.get("fecha_alarma").split(" ")[2]
            fecha_i = datetime.datetime(int(fecha_i.split("-")[0]),int(fecha_i.split("-")[1]),int(fecha_i.split("-")[2]))
            fecha_f = datetime.datetime(int(fecha_f.split("-")[0]),int(fecha_f.split("-")[1]),int(fecha_f.split("-")[2]))
            desc = ""
            try:
                desc = request.POST.get("descripcion")
            except Exception:
                pass
            for i in Alarma.objects.filter(id_refeer = refeer).all():
                for t in AlarmaContacto.objects.filter(id_alarma=i).all():
                    t.status=False
                    t.save()
                i.on = False
                i.save()
            cont = 0
            alarma = Alarma.objects.create(
                inicio = fecha_i,
                fin = fecha_f,
                id_refeer = refeer,
                aire_tierra = int(request.POST.get("nombre_temp")),
                treshhold = int(request.POST.get("inferior")),
                on = True,
                desc = desc,
                color = request.POST.get("color_alarma"),
                id_user = request.user
            )
            for i in User.objects.all():
                name_string = "user-"+str(i.id)
                if request.POST.get(name_string):
                    AlarmaContacto.objects.create(
                        id_user = i,
                        id_alarma = alarma
                    )
                    print("Alarma contacto crreada")
            
        elif request.POST.get("hora"):
            timeframe = int(request.POST.get("timeframe"))
            get_last_lecturas_refeer(refeer,context,timeframe)
        elif request.POST.get("ciclo"):
            create_ciclo(request,refeer)
            fecha_i = request.POST.get("fecha_ciclo").split(" ")[0] 
            fecha_f = request.POST.get("fecha_ciclo").split(" ")[2]
            fecha_i = datetime.datetime(int(fecha_i.split("-")[0]),int(fecha_i.split("-")[1]),int(fecha_i.split("-")[2]))
            fecha_f = datetime.datetime(int(fecha_f.split("-")[0]),int(fecha_f.split("-")[1]),int(fecha_f.split("-")[2]))
            temp_1 = int(request.POST.get("temp_ciclo").split("-")[0].strip().replace("T",""))
            temp_2 = int(request.POST.get("temp_ciclo").split("-")[1].strip().replace("T",""))
            fecha_fin_subciclo = get_fecha_from_input_1(request.POST.get("fin_subciclo"))
            string_fechas_sub = str(fecha_i) + "--" + str(fecha_fin_subciclo) + ";"
            Ciclo.objects.create(
                subciclos = request.POST.get("temp_ciclo"),
                subfechas = string_fechas_sub,
                inicio = fecha_i,
                fin = fecha_f,
                observacion = request.POST.get("obs"),
                id_refeer = refeer,
                id_user = request.user
            )
            print("subciclo y ciclo creados")
        elif request.POST.get("subciclo"):   
            id_ciclo =  int(request.POST.get("ciclo_id"))
            ciclo = Ciclo.objects.filter(id_ciclo = id_ciclo).first()
        
    context['Alarma_activa'] = Alarma.objects.filter(id_refeer = refeer).order_by("-created").first()
    context['alarmas_historicas'] = Alarma.objects.filter(id_refeer = refeer).order_by("-created")[:10]
    context['ciclo'] = Ciclo.objects.filter(id_refeer = refeer).order_by("-timestamp").first()
    print(context['ciclo'])
    context['users'] = User.objects.all()
    html_template = loader.get_template('home/refeer.html')
    return HttpResponse(html_template.render(context, request))

def input_lectura(request):
    if request.method == 'GET':
        refeer = Refeer.objects.filter(id_refeer = 1).first()
        LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp1")),
            sensor = 1,
            id_refeer = refeer
        )
        try:
            LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp2")),
            sensor = 2,
            id_refeer = refeer
        )
        except Exception:
            pass
        try:
            LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp3")),
            sensor = 3,
            id_refeer = refeer
        )
        except Exception:
            pass
        try:
            LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp4")),
            sensor = 4,
            id_refeer = refeer
        )
        except Exception:
            pass
        try:
            LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp5")),
            sensor = 5,
            id_refeer = refeer
        )
        except Exception:
            pass
        try:
            LecturaRefeer.objects.create(
            lectura = int(request.GET.get("temp6")),
            sensor = 6,
            id_refeer = refeer
        )
        except Exception:
            pass
        print("input conexitoo")
    context = {}
    html_template = loader.get_template('home/input.html')
    return HttpResponse(html_template.render(context, request))
def lectura(request,id_refeer,id_sensor):
    if request.method=='GET':
        try:
            refeer = Refeer.objects.filter(id_refeer = int(request.POST.get("refeer"))).first()
            LecturaRefeer.objects.create(
                lectura = int(request.GET.get("temperatura")),
                es_tierra = bool(int(request.GET.get("tierra"))),
                sensor = id_sensor,
                id_refeer =refeer
            )
            print("lectura creada")
        except Exception:
            print("error de lectura")

def create_ciclo(request,refeer):
    user = request.user
    
    
@login_required(login_url="/login/")
def administrador(request):
    context = {}
    context['refeers'] = Refeer.objects.all()
    if request.method == 'POST':
        if request.POST.get("grafico"):
            if request.POST.get("tipo_grafico") == 'HORAS':
                refeer = int(request.POST.get("refeer"))
                entries = int(request.POST.get("entries"))
                get_last_lecturas_refeer(refeer,context,entries)
                count_lecturas = LecturaRefeer.objects.filter(id_refeer = refeer).all().count()
                context['lecturas'] = LecturaRefeer.objects.filter(id_refeer = refeer).order_by("-created")[(count_lecturas)-entries:]
                print(context['lecturas'])
            if request.POST.get("tipo_grafico") == 'DIAS':
                pass
            print("grafico")
    html_template = loader.get_template('home/administrador.html')
    return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment     = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment     = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboards-'):
            active_menu = 'dashboard'

        if segment.startswith('account-') or segment.startswith('users-') or segment.startswith('profile-') or segment.startswith('projects-'):
            active_menu = 'pages'

        if  segment.startswith('notifications') or segment.startswith('sweet-alerts') or segment.startswith('charts.html') or segment.startswith('widgets') or segment.startswith('pricing'):
            active_menu = 'pages'            

        return segment, active_menu     

    except:
        return 'index', 'dashboard'  
