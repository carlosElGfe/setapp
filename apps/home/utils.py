from .models import *
import datetime
def get_last_lecturas_refeer(refeer,context,size):
    lectura_1 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 1).order_by("-created")
    lectura_1 = lectura_1[len(lectura_1)-size:]
    lectura_2 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 2).order_by("-created")
    lectura_2 = lectura_2[len(lectura_2)-size:]
    lectura_3 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 3).order_by("-created")
    lectura_3 = lectura_3[len(lectura_3)-size:]
    lectura_4 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 4).order_by("-created")
    lectura_4 = lectura_4[len(lectura_4)-size:]
    lectura_5 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 5).order_by("-created")
    lectura_5 = lectura_5[len(lectura_5)-size:]
    lectura_6 = LecturaRefeer.objects.filter(id_refeer = refeer,sensor = 6).order_by("-created")
    lectura_6 = lectura_6[len(lectura_6)-size:]
    lectura_1_t = list(map(lambda x: x.lectura,lectura_1))
    context['tiempos'] = list(map(lambda x: x.created,lectura_1))
    lectura_2_t = list(map(lambda x: x.lectura,lectura_2))
    lectura_3_t = list(map(lambda x: x.lectura,lectura_3))
    lectura_4_t = list(map(lambda x: x.lectura,lectura_4))
    lectura_5_t = list(map(lambda x: x.lectura,lectura_5))
    lectura_6_t = list(map(lambda x: x.lectura,lectura_6))
    avg = []
    avg2 = []
    for i in range(0,size):
        total = 0
        total2 = 0
        total += lectura_1_t[i]
        total += lectura_2_t[i]
        total += lectura_3_t[i]
        total += lectura_4_t[i]
        total2 += lectura_5_t[i]
        total2 += lectura_6_t[i]
        total = (total/4)
        total2 = (total2/2)
        avg.append(total)
        avg2.append(total2)
    context['avg'] = avg
    context['avg2'] = avg2
    context['L1'] = lectura_1_t
    context['L2'] = lectura_2_t
    context['L3'] = lectura_3_t
    context['L4'] = lectura_4_t
    context['L5'] = lectura_5_t
    context['L6'] = lectura_6_t
   
def get_my_homework():
    tareas = []
    for i in Alarma.objects.filter(on=True):
        fecha1 = prepare_fecha_calendar(i.inicio) 
        fecha2 = prepare_fecha_calendar_fin(i.fin) 
        nombre = " Refeer "+ str(i.id_refeer.id_refeer)
        buffer = []
        buffer.append(fecha1)
        buffer.append(fecha2)
        buffer.append(nombre)
        buffer.append(i.color)
        tareas.append(buffer)
    return tareas 

def prepare_fecha_calendar(fecha):
    fecha2 = str(fecha)
    try:
        dia = str(fecha2).split(" ")[0].split("-")[2]
        mes = str(fecha2).split(" ")[0].split("-")[1]
        ano = str(fecha2).split(" ")[0].split("-")[0]
        return str(ano)+"-"+mes+"-"+dia
    except Exception:
        return 0

def prepare_fecha_calendar_fin(fecha):
    fecha2 = str(fecha)
    try:
        dia = str(fecha2).split(" ")[0].split("-")[2]
        mes = str(fecha2).split(" ")[0].split("-")[1]
        ano = str(fecha2).split(" ")[0].split("-")[0]
        return str(ano)+"-"+mes+"-"+str(int(dia)+1)
    except Exception:
        return 0

def get_fecha_actual():
    ano = int(datetime.datetime.now().year)
    mes = int(datetime.datetime.now().month)
    dia = int(datetime.datetime.now().day)
    mes = get_right(mes)
    dia = get_right(dia)
    fecha_actual = str(ano)+"-"+str(mes)+"-"+str(dia)
    return fecha_actual

def get_right(num):
    if (num//10) == 0:
        return "0"+str(num)
    else:
        return str(num)
    
def get_fecha_from_input_1(fecha):
    fecha = fecha.split("-")
    fecha = datetime.datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]))
    return fecha
    
def get_fecha_from_input(fecha,fecha2):
    fecha = fecha.split("-")
    fecha = datetime.datetime(int(fecha[0]),int(fecha[1]),int(fecha[2]))
    fecha2 = fecha2.split("-")
    fecha2 = datetime.datetime(int(fecha2[0]),int(fecha2[1]),int(fecha2[2]))
    return fecha,fecha2