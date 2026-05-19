from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ==============================
    # HOME
    # ==============================

    path('', views.home, name='home'),
    
    # ==============================
    # USUARIOS
    # ==============================

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),
    
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    
    path(
        'registro/',
        views.registro_usuario,
        name='registro_usuario'
    ),


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
        'habitos/<str:tipo>/<int:habito_id>/',
        views.detalle_habito,
        name='detalle_habito'
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

    path(
        'registros/crear/<str:tipo>/<int:habito_id>/',
        views.crear_registro,
        name='crear_registro'
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
        'estadisticas/<str:tipo>/<int:habito_id>/',
        views.estadisticas_por_tipo,
        name='estadisticas_por_tipo'
    ),

    path(
        'estadisticas_global/',
        views.estadisticas_global,
        name='estadisticas_global'),

    # ==============================
    # EXPORTAR IMPORTAR
    # ==============================

    path(
        'exportar/json/',
        views.exportar_json,
        name='exportar_json'
    ),

    path(
        'importar/json/',
        views.importar_json,
        name='importar_json'
    ),
]
