from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.contrib import messages
from home.models import *#base de datos
from acceso.decorators import logueado #decorador para traer metadata_id
from utilidades import utilidades,webpay
import json
from django.conf import settings

@logueado()
def carro_inicio(request):
    cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    datos = Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    return render(request,'carro/home.html',{'datos':datos,'suma':suma,'cuantos':cuantos})



@logueado()
def carro_crear(request):
    if request.method =='POST':
        try:
            datos=Producto.objects.filter(pk=request.POST['id']).get()
        except Producto.DoesNotExist:
            raise Http404
        Carrito.objects.create(cantidad=request.POST['cantidad'],producto_id=request.POST['id'],users_metadata_id=request.session['users_metadata_id'])
        return HttpResponseRedirect("/carro")
    else:
        raise Http404

@logueado()
def carro_vaciar(request):
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).delete
    OrdenDeCompra.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(estado_id=3).delete()
    messages.add_message(request,messages.SUCCESS,f'Se vacio tu carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')


@logueado()
def carro_quitar(request,id):
    try:
        datos=Producto.objects.filter(pk=id).get()
    except Producto.DoesNotExist:
        raise Http404
    Carrito.objects.filter(user_metadata_id=request['user_metadata_id']).filter(producto_id=id).delete()
    messages.add_message(request,messages.SUCCESS,f'Se quito el producto del carrito exitosamente')
    return HttpResponseRedirect('/carro')

@logueado()
def carro_modificar_cantidad(request,id,cantidad):
    try:
        datos=Carrito.objects.filter(pk=id).get()
    except Carrito.DoesNotExist:
        raise Http404
    Carrito.objects.filter(id=id).update(cantidad=cantidad)
    messages.add_message(request,messages.SUCCESS,f'Se modifico la cantidad del producto{datos.producto.nombre}exitosamente!!!.')
    return HttpResponseRedirect('/carro')

@logueado()
def carro_pagar(request):
    cuantos =Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    if cuantos ==0:
        return HttpResponseRedirect('/carro')
    datos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()

    suma=0

    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor

    usuario=UserMetadata.objects.filter(id=request.session['users_metadata_id']).get()
    comunas=Comuna.objects.all()
    return render(request,'carro/pagar.html',{'datos':datos,'suma':suma,'usuario':usuario,'comunas':comunas,'cuantos':cuantos})

@logueado()
def carro_webpay(request):
    if request.method =='POST':
        cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
        if cuantos==0:
            return HttpResponseRedirect('/carro')
        direccion=f"{request.POST['direccion']}{request.POST['indicaciones']}"
        result=webpay.crearTransaccion(request.session['users_metadata_id'],direccion,request.POST['comuna'])
        return render(request,'carro/webpay.html',{'url':result['url'],'token':result['token']})

@logueado()
def carro_web_pay_respuesta(request):
    if not request.GET.get('token_ws'):
        raise Http404
    token=request.GET.get('token_ws')
    result=webpay.verificarTransaccion(token)
    if result[0]=='vacio':
        raise Http404
    if result[0]=='AUTHORIZED':
        try:
            orden=OrdenDeCompra.objects.filter(users_metadata_id=request.session['users_metadata_id'],estado_id=3).get()
        except OrdenDeCompra.DoesNotExist:
            raise Http404
        OrdenDeCompra.objects.filter(users_metadata_id=request.session['user_metadata_id'],estado_transbank=0).update(token_ws=token, estado_transbank=result[0],fecha_transbank=result[2],tarjeta=result[1],estado_id=6)
        suma=0
        datos=Carrito.objects.filter(user_metadata_id=request.session['users_metadata_id']).all()
        detalle=""
        for dato in datos:
            valor=dato.cantidad*dato.producto.precio
            suma=suma+valor
            detalle=f"""{detalle}
            <tr>
                <td style="border: 1px solid black;">
                <img src="{settings.BASE_URL}assets/upload/producto/{dato.producto.foto}"width="100" height="100">
                </td>
                <td style="border: 1px solid black;">{dato.producto.nombre}s</td>
                <td style="border: 1px solid black;">{dato.cantidad}</td>
                <td style="border: 1px solid black;">{utilidades.numberFormat(dato.producto.precio)}</td>
            </tr>
            """
            OrdenDeCompra.objects.create(orden_de_compra_id=orden.id,producto_id=dato.producto_id,cantidad=dato.cantidad)
            Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).delete()
            usuario=UserMetadata.objects.filter(id=request.session['users_metadata_id']).get()
            messages.add_message(request,messages.SUCCESS,f'La orden de compra N°{orden.id} ha sido generada exitosamente. Tu numero de transaccion de transbank es {token}.Nos pondremos en contacto contigo en la brevedad para coordinar el envio de los productos.Gracias por tu compra!!!')
            return HttpResponseRedirect('/carro')
        if result[0]=='FAILED':
            OrdenDeCompra.objects.filter(users_metadata_id=request.session)['users_metadata_id'].filter(estado_transbank=0).update(token_ws=token,fecha_transbank=result[2],tarjeta=result[1],estado_id=5)
            messages.add_message(request,messages.WARNING,f'No fue posible procesar el pago, por favor vuelva a intentarlo!.')
            return HttpResponseRedirect('/carro')
