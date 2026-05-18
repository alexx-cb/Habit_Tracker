from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    HabitoBooleano,
    HabitoContador,
    HabitoSemanal,
    Registro
)

from .forms import (
    HabitoBooleanoForm,
    HabitoContadorForm,
    HabitoSemanalForm,
    RegistroForm
)

from .services.analizador import AnalizadorHabitos


TIPOS_HABITO = {
    'booleano': HabitoBooleano,
    'contador': HabitoContador,
    'semanal': HabitoSemanal,
}


def _obtener_modelo_habito(tipo):
    modelo = TIPOS_HABITO.get(tipo)
    if modelo is None:
        raise Http404('Tipo de habito no valido')
    return modelo


def _obtener_habito(tipo, habito_id):
    return get_object_or_404(_obtener_modelo_habito(tipo), id=habito_id)


def _obtener_tipo_habito(habito):
    if isinstance(habito, HabitoBooleano):
        return 'booleano'
    if isinstance(habito, HabitoContador):
        return 'contador'
    if isinstance(habito, HabitoSemanal):
        return 'semanal'
    raise ValueError('Tipo de habito no soportado')


def _contar_registros_cumplidos(habito, registros):
    if isinstance(habito, HabitoContador):
        return sum(
            1 for registro in registros
            if (registro.valor or 0) >= habito.objetivo_diario
        )

    return registros.filter(cumplido=True).count()


# ======================================
# HOME
# ======================================

def home(request):

    total_habitos = (
        HabitoBooleano.objects.count() +
        HabitoContador.objects.count() +
        HabitoSemanal.objects.count()
    )

    total_registros = Registro.objects.count()

    habitos_activos = (
        HabitoBooleano.objects.filter(activo=True).count() +
        HabitoContador.objects.filter(activo=True).count() +
        HabitoSemanal.objects.filter(activo=True).count()
    )

    habitos = (
        list(HabitoBooleano.objects.all()) +
        list(HabitoContador.objects.all()) +
        list(HabitoSemanal.objects.all())
    )

    if habitos:
        promedio_progreso = round(
            sum(h.calcular_progreso() for h in habitos) / len(habitos),
            2
        )
    else:
        promedio_progreso = 0

    ultimos_habitos = sorted(
        habitos,
        key=lambda h: h.fecha_inicio,
        reverse=True
    )[:5]

    ultimos_habitos = [
        {
            'obj': habito,
            'tipo': _obtener_tipo_habito(habito)
        }
        for habito in ultimos_habitos
    ]

    return render(request, 'home.html', {
        'total_habitos': total_habitos,
        'total_registros': total_registros,
        'habitos_activos': habitos_activos,
        'promedio_progreso': promedio_progreso,
        'ultimos_habitos': ultimos_habitos
    })


# ======================================
# LISTA HÁBITOS
# ======================================

def lista_habitos(request):

    return render(request, 'habitos/lista_habitos.html', {
        'habitos_booleanos': HabitoBooleano.objects.all(),
        'habitos_contador': HabitoContador.objects.all(),
        'habitos_semanales': HabitoSemanal.objects.all()
    })


# ======================================
# CREAR HÁBITO
# ======================================

def seleccionar_tipo_habito(request):
    return render(request, 'habitos/seleccionar_tipo.html')


def crear_habito_booleano(request):

    form = HabitoBooleanoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_habitos')

    return render(request, 'habitos/crear_habito.html', {'form': form})


def crear_habito_contador(request):

    form = HabitoContadorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_habitos')

    return render(request, 'habitos/crear_habito.html', {'form': form})


def crear_habito_semanal(request):

    form = HabitoSemanalForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_habitos')

    return render(request, 'habitos/crear_habito.html', {'form': form})


# ======================================
# DETALLE HÁBITO BOOLEANO (puedes replicar para otros tipos)
# ======================================

def detalle_habito(request, tipo, habito_id):

    habito = _obtener_habito(tipo, habito_id)

    return render(request, 'habitos/detalle_habito.html', {
        'habito': habito,
        'tipo_habito': tipo,
        'registros': habito.registros.all(),
        'progreso': habito.calcular_progreso()
    })


def detalle_habito_booleano(request, habito_id):
    return detalle_habito(request, 'booleano', habito_id)


# ======================================
# REGISTROS
# ======================================

def crear_registro(request, tipo, habito_id):

    habito = _obtener_habito(tipo, habito_id)

    form = RegistroForm(request.POST or None)
    setattr(form.instance, f'habito_{tipo}', habito)

    if form.is_valid():
        registro = form.save()
        return redirect('detalle_habito', tipo=tipo, habito_id=habito.id)

    return render(request, 'registros/crear_registro.html', {
        'form': form,
        'habito': habito,
        'tipo_habito': tipo
    })


def crear_registro_booleano(request, habito_id):
    return crear_registro(request, 'booleano', habito_id)


def crear_registro_contador(request, habito_id):
    return crear_registro(request, 'contador', habito_id)


def crear_registro_semanal(request, habito_id):
    return crear_registro(request, 'semanal', habito_id)


def lista_registros(request):

    return render(request, 'registros/lista_registros.html', {
        'registros': Registro.objects.all().order_by('-fecha')
    })


# ======================================
# ESTADÍSTICAS
# ======================================

def estadisticas(request, habito_id):
    return estadisticas_por_tipo(request, 'booleano', habito_id)


def estadisticas_por_tipo(request, tipo, habito_id):

    habito = _obtener_habito(tipo, habito_id)

    registros = habito.registros.all().order_by('-fecha')

    porcentaje = round(habito.calcular_progreso(), 2)
    racha = AnalizadorHabitos.calcular_racha_actual(habito)

    # datos extra para análisis
    total_registros = registros.count()
    cumplidos = _contar_registros_cumplidos(habito, registros)

    tasa = (cumplidos / total_registros * 100) if total_registros > 0 else 0

    return render(request, 'habitos/estadisticas.html', {
        'habito': habito,
        'tipo_habito': tipo,
        'porcentaje': porcentaje,
        'racha': racha,
        'total_registros': total_registros,
        'cumplidos': cumplidos,
        'tasa': tasa,
        'registros': registros
    })


def estadisticas_global(request):

    habitos = (
        list(HabitoBooleano.objects.all()) +
        list(HabitoContador.objects.all()) +
        list(HabitoSemanal.objects.all())
    )
    habitos_con_tipo = []

    for h in habitos:
        habitos_con_tipo.append({
            "obj": h,
            "tipo": _obtener_tipo_habito(h),
            "id": h.id,
            "nombre": h.nombre,
            "progreso": h.calcular_progreso()
        })

    total = sum(h["progreso"] for h in habitos_con_tipo)
    promedio = total / len(habitos_con_tipo) if habitos_con_tipo else 0

    return render(request, "habitos/estadisticas_global.html", {
        "total": promedio,
        "habitos": habitos_con_tipo
    })


# ======================================
# ELIMINAR
# ======================================

def eliminar_habito_booleano(request, habito_id):

    habito = get_object_or_404(HabitoBooleano, id=habito_id)

    if request.method == 'POST':
        habito.delete()
        return redirect('lista_habitos')

    return render(request, 'habitos/eliminar_habito.html', {
        'habito': habito
    })
