from functools import wraps
from django.contrib.auth import authenticate
from home.models import *
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from utilidades import utilidades

def logueado():
    def _activo_required(func):
        @wraps(func)
        def _decorator(request,*args,**kwargs):
            if not request.user.is_authenticated:
                messages.add_message(request,messages.WARNING,'Debes estar logueado para visualizar este contenido.')
                return HttpResponseRedirect('/formularios/login')
            else:
                usersMetadata = UserMetadata.objects.filter(user_id=request.user.id).get()
                request.session['users_metadata_id']=usersMetadata.id
                return func(request,*args,**kwargs)
        return _decorator
    return _activo_required




# def ejemplo():
#     def _activo_required(func):
#         @wraps(func)
#         def _decorator(request,*args,**kwargs):
                #aca haces tu magia
#             pass
#         return _decorator
#     return _activo_required