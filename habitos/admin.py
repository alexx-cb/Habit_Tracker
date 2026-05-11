from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(HabitoBooleano)
admin.site.register(HabitoContador)
admin.site.register(HabitoSemanal)
admin.site.register(Registro)