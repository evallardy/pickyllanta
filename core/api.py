from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from django.http import JsonResponse
import json

@api_view(['POST','GET','PULL','PUT','PATCH','DELETE'])
def mensaje_api_view(request):
    # Guardado de la información que llega tanto el meodo como la información
#    bitacora = bitacora(descripcion = json.dumps(request.data)[0:254])
#    bitacora.save()

    if request.method == 'POST' and request.data:
        datos = request.data
        if datos['number'] and datos['message-in'] and datos['message_in_raw'] \
            and datos['application'] and datos['type']:
            numero = datos['number']
            message_in = datos['message-in']
            message_in_raw = datos['message_in_raw']
            application = datos['application']
            tipo = datos['type']
            opcion_seleccionada = message_in_raw
            # Busca comunicacion
            comunicacion = MensajePicky.objects.filter(number=numero,estatus_mensaje=1).last()
            message = ""
            respuesta = ""
            if comunicacion:
                # quitar espacion en la cadena del mensaje
                opcion_sel = opcion_seleccionada.upper().replace(" ", "")
                nivel = comunicacion.nivel
                pk = comunicacion.id
                if buscaOpcion(comunicacion, opcion_sel):
                    if opcion_sel == 'R':
                        # Envia menu anteriror
                        sig_comunicacion = MensajePicky.objects.filter(id=pk).update(nivel=nivel-1)
                        menu_json = traeJson(comunicacion, nivel-1)
                        message = creaMenu(json.dumps(menu_json))
                    elif opcion_sel == 'X':
                        sig_comunicacion = MensajePicky.objects.filter(id=pk).update(estatus_mensaje=0)
                        message = "Gracias por su preferencia, lo esperamos muy pronto \n\n"
                    else:
                        menu_json = traeJson(comunicacion, nivel)
                        if int(opcion_sel) < 10:
                            numero = f"  {opcion_sel}"
                        elif int(registro) < 100:
                            numero = f" {opcion_sel}"
                        else:
                            numero = str(opcion_sel)
                        menu_json['seleccion'] = numero
                        menu_json1 = generaJson(comunicacion, nivel + 1)
                        if nivel == 1:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion1=menu_json, opcion2=menu_json1, nivel=nivel+1)
                        elif nivel == 2:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion2=menu_json, opcion3=menu_json1, nivel=nivel+1)
                        elif nivel == 3:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion3=menu_json, opcion4=menu_json1, nivel=nivel+1)
                        elif nivel == 4:
                            upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion4=menu_json, opcion5=menu_json1, nivel=nivel+1)
                        message = creaMenu(json.dumps(menu_json1))
                else:
                    # Envia nuevamente el mismo menu
                    menu_json = traeJson(comunicacion, nivel)
                    message = creaMenu(json.dumps(menu_json))
            else:
                #  Crea el menu primer nivel
                menu_json = generaJson(None, 1)
                message = creaMenu(json.dumps(menu_json))
                
                # Guarda la peticion la primera vez con su primer menu
                comunicacion = MensajePicky(
                    number = numero,
                    message_in = message_in,
                    message_in_raw = message_in_raw,
                    application = application,
                    tipo = tipo,
                    nivel=1,
                    opcion1 = menu_json,
                )
                comunicacion.save()
            # Se envia repuesta 
            respuesta = {"number":numero,"application":application,"message":message,"type":tipo, "message-out":message,"delay":"0"}
            return Response(respuesta)
        else:
            # Se envia el mensaje de error, no envian nada
            if datos['number']:
                respuesta = mensajeError(datos['number'])
            else:
                respuesta = mensajeError("Faltan datos")
            return Response(respuesta)
    else:
        # Se envia el mensaje de error, no envian nada
        respuesta = mensajeError("Sin número")
        return Response(respuesta)
                
def generaJson(comunicacion, nivel):
    opciones = {}
    titulo = ""
    if nivel == 1:
        titulo = "Hola! 👋 Bienvenido al sistema de cotización *Automatizada* de LlantaShop.com 🤖 \n" + \
        "Comencemos, \n" + \
        "➡️ escribe el Ancho de llanta que buscas, son los primeros 3 digitos de tu medida."
        ancho_distinct = Llanta.objects.filter(alto__gt=0, rin__gt=0).values_list('ancho', flat=True).distinct().order_by('ancho')
        registro = 0
        if ancho_distinct:
            for ancho in ancho_distinct:
                registro += 1
                if registro < 10:
                    numero = f"  {registro}"
                elif registro < 100:
                    numero = f" {registro}"
                else:
                    numero = str(registro)
                opciones[numero] = ancho
        opciones['X'] = 'Terminar'
    elif nivel == 2:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        titulo = "Los altos disponibles para el ancho '255' son:\n\n"
        alto_distinct = Llanta.objects.filter(ancho=ancho, rin__gt=0).values_list('alto', flat=True).distinct().order_by('alto')
        registro = 0
        if alto_distinct:
            for alto in alto_distinct:
                registro += 1
                if registro < 10:
                    numero = f"  {registro}"
                elif registro < 100:
                    numero = f" {registro}"
                else:
                    numero = str(registro)
                opciones[numero] = alto
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 3:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        titulo = "Los Diámetros de Rin disponibles para el ancho '255' con alto '75' son:\n\n"
        rin_distinct = Llanta.objects.filter(ancho=ancho, alto=alto).values_list('rin', flat=True).distinct().order_by('rin')
        registro = 0
        if rin_distinct:
            for rin in rin_distinct:
                registro += 1
                if registro < 10:
                    numero = f"  {registro}"
                elif registro < 100:
                    numero = f" {registro}"
                else:
                    numero = str(registro)
                opciones[numero] = rin
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    else:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        rin = opcionSeleccionadaT(comunicacion, 3)
        rinN = opcionSeleccionada(comunicacion, 3)
        titulo = '📶 Estas son las Marcas y Modelos que tenemos disponibles para entrega inmediata,escoge el que mas te guste y se ajuste a tu presupuesto!\n\n'
        llantas_seleccionadas = Llanta.objects.filter(ancho=ancho, alto=alto, rin=rin)
        registro = 0
        if llantas_seleccionadas:
            for llanta in llantas_seleccionadas:
                registro += 1
                if registro < 10:
                    numero = f"  {registro}"
                elif registro < 100:
                    numero = f" {registro}"
                else:
                    numero = str(registro)
#                opciones[registro] = "*Desc:*  " + llanta.descripcion + "\n*Exist:* " + str(llanta.existencia) + "\n*Precio contado: " + str(llanta.precio_especia_llantashop_pago_efectivo) + "*"
                opciones[numero] = "*Desc:*  {}\n*Exist:* {}\n*Precio contado: {}*".format(
                    llanta.descripcion,
                    llanta.existencia,
                    "${:,.2f}".format(llanta.precio_especia_llantashop_pago_efectivo)
                )
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    data = {'titulo': titulo, 'seleccion':0, 'opciones': opciones}
    return data

def buscaOpcion(comunicacion, opcion_sel):
    nivel = comunicacion.nivel
    menu_json = traeJson(comunicacion, nivel)
    return existeOpcion(menu_json, opcion_sel)

def traeJson(comunicacion, opcion):
    if opcion == 1:
        menu_json = comunicacion.opcion1
    elif opcion == 2:
        menu_json = comunicacion.opcion2
    elif opcion == 3:
        menu_json = comunicacion.opcion3
    elif opcion == 4:
        menu_json = comunicacion.opcion4
    else:
        menu_json = comunicacion.opcion5
    return menu_json

def existeOpcion(menu_json, opcion_sel):
    encontro = False
    for opcion in menu_json['opciones']:
        if opcion.strip() == opcion_sel.strip():
            encontro = True
            break
    return encontro
                
def opcionSeleccionada(comunicacion, opcion):
    opcion_sel = traeJson(comunicacion, opcion)
    seleccion = opcion_sel['seleccion']
    return seleccion

def opcionSeleccionadaT(comunicacion, opcion):
    opcion_sel = traeJson(comunicacion, opcion)
    seleccion = opcion_sel['seleccion']
    return opcion_sel['opciones'][seleccion]

def creaMenu(objeto):
    json_data = json.loads(objeto)
    mensaje = json_data['titulo']
    if json_data['opciones']:
        opcs = json_data['opciones']
        opciones = {k: v for k, v in sorted(opcs.items())}
        for opcion in opciones:
            mensaje += opcion + " - " + opciones[opcion] + "\n"
    return mensaje

def mensajeError(numeroTelefono):
    mensaje = 'Faltan datos'
    respuesta = {'Error':mensaje}
    bitacora = Bitacora(descripcion = "Celular:" + numeroTelefono + "/" + mensaje)
    bitacora.save()
    return respuesta
