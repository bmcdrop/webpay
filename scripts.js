function confirmaAlert(pregunta,ruta){
    jCustomConfirm(pregunta,'Tienda','Aceptar','Cancelar',function(r){
        if (r){
            window.location=ruta;
        }
    });
}

function alertAlert(mensaje){
    jAlert(mensaje);
}

function agregarAlCarro()
{
    var form = document.agregar_al_carro;
    form.cantidad.value=document.getElementById('cantidad').value;
    form.submit();
}

function sendLogin(){
    var form=document.form_login;
    if(form.correo.value==0)
    {
        alertAlert('El campo E-Mail es obligatorio');
        form.correo.value='';
        return false;
    }
    if(validaCorreo(form.correo.value)==false)
    {
        alertAlert('E-Mail no es valido');
        form.correo.value='';
        return false;
    }
    if(form.password.value==0)
    {
        alertAlert('El campo Contraseña es obligatorio');
        form.password.value='';
        return false;
    }
    form.submit();
}

function sendRegistro()
{
    form=document.form_registro;
    if(form.nombre.value==0)
    {
        alertAlert('El campo Nombre es obligatorio');
        form.nombre.value='';
        return false;
    }
    if(form.apellido.value==0)
    {
        alertAlert('El campo Apellido es obligatorio');
        form.apellido.value='';
        return false;
    }
    if(form.correo.value==0)
    {
        alertAlert('El campo E-Mail es obligorio')
        form.correo.value='';
        return false;
    }
    if(validaCorreo(form.correo.value)==false)
    {
        alertAlert('El E-Mail no es valido');
        form.correo.value='';
        return false;
    }
    if(form.password.value==0)
    {
        alertAlert('El campo Contraseña es obligatorio');
        form.password.value='';
        return false;
    }
    if(form.password2.value==0)
    {
        alertAlert('El campo Repetir Contraseña es obligatorio');
        form.password2.value='';
        return false;
    }
    if(form.password.value!=form.password2.value)
    {
        alertAlert('Las contraseñas no coinciden');
        form.password.value='';
        form.password2.value='';
        return false;
    }
    form.submit();

}

function sendPago()
{
    let form=document.form_pagar;
    if(form.direccion.value==0)
    {
        alertAlert("Debes indicar la direccion del envio");
        return false;
    }
    if(form.indicaciones.value==0)
    {
        form.indicaciones.value="";

    }
    form.submit();
}