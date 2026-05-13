from django.urls import path
from . import views

urlpatterns = [

    # ==============================
    # HOME
    # ==============================

    path('', views.home, name='home'),


    # ==============================
    # HÁBITOS
    # ==============================

    path(
        'habitos/',
        views.lista_habitos,
        name='lista_habitos'
    ),

    path(
        'habitos/crear/',
        views.seleccionar_tipo_habito,
        name='seleccionar_tipo_habito'
    ),

    path(
        'habitos/crear/booleano/',
        views.crear_habito_booleano,
        name='crear_habito_booleano'
    ),

    path(
        'habitos/crear/contador/',
        views.crear_habito_contador,
        name='crear_habito_contador'
    ),

    path(
        'habitos/crear/semanal/',
        views.crear_habito_semanal,
        name='crear_habito_semanal'
    ),

    path(
        'habitos/<int:habito_id>/',
        views.detalle_habito_booleano,
        name='detalle_habito_booleano'
    ),

    path(
        'habitos/<int:habito_id>/eliminar/',
        views.eliminar_habito_booleano,
        name='eliminar_habito_booleano'
    ),


    # ==============================
    # REGISTROS
    # ==============================

    path(
        'registros/',
        views.lista_registros,
        name='lista_registros'
    ),

    path(
        'registros/crear/<int:habito_id>/',
        views.crear_registro_booleano,
        name='crear_registro_booleano'
    ),


    # ==============================
    # ESTADÍSTICAS
    # ==============================

    path(
        'estadisticas/<int:habito_id>/',
        views.estadisticas,
        name='estadisticas'
    ),

    path(
        'estadisticas_global/',
        views.estadisticas_global,
        name='estadisticas_global'),
]