from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

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

    context = {
        'total_habitos': total_habitos,
        'total_registros': total_registros
    }

    return render(request, 'home.html')



# ======================================
# LISTA HÁBITOS
# ======================================


def lista_habitos(request):

    habitos_booleanos = HabitoBooleano.objects.all()
    habitos_contador = HabitoContador.objects.all()
    habitos_semanales = HabitoSemanal.objects.all()

    context = {
        'habitos_booleanos': habitos_booleanos,
        'habitos_contador': habitos_contador,
        'habitos_semanales': habitos_semanales
    }

    return render(
        request,
        'habitos/lista_habitos.html',
        context
    )


# ======================================
# CREAR HABITO
# ======================================
def seleccionar_tipo_habito(request):
    return render(request, 'habitos/seleccionar_tipo.html')


# ======================================
# CREAR HÁBITO BOOLEANO
# ======================================


def crear_habito_booleano(request):

    if request.method == 'POST':

        form = HabitoBooleanoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_habitos')

    else:
        form = HabitoBooleanoForm()

    return render(
        request,
        'habitos/crear_habito.html',
        {'form': form}
    )


# ======================================
# CREAR HÁBITO CONTADOR
# ======================================


def crear_habito_contador(request):

    if request.method == 'POST':

        form = HabitoContadorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_habitos')

    else:
        form = HabitoContadorForm()

    return render(
        request,
        'habitos/crear_habito.html',
        {'form': form}
    )



# ======================================
# CREAR HÁBITO SEMANAL
# ======================================


def crear_habito_semanal(request):

    if request.method == 'POST':

        form = HabitoSemanalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_habitos')

    else:
        form = HabitoSemanalForm()

    return render(
        request,
        'habitos/crear_habito.html',
        {'form': form}
    )

# ======================================
# DETALLE HÁBITO BOOLEANO
# ======================================


def detalle_habito_booleano(request, habito_id):

    habito = get_object_or_404(
        HabitoBooleano,
        id=habito_id
    )

    registros = habito.registros.all()

    progreso = habito.calcular_progreso()

    context = {
        'habito': habito,
        'registros': registros,
        'progreso': progreso
    }

    return render(
        request,
        'habitos/detalle_habito.html',
        context
    )



# ======================================
# CREAR REGISTRO
# ======================================


def crear_registro_booleano(request, habito_id):

    habito = get_object_or_404(
        HabitoBooleano,
        id=habito_id
    )

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            registro = form.save(commit=False)

            registro.habito = habito

            registro.save()

            return redirect(
                'detalle_habito_booleano',
                habito_id=habito.id
            )

    else:
        form = RegistroForm()

    return render(
        request,
        'registros/crear_registro.html',
        {
            'form': form,
            'habito': habito
        }
    )



# ======================================
# LISTA REGISTROS
# ======================================


def lista_registros(request):

    registros = Registro.objects.all().order_by('-fecha')

    return render(
        request,
        'registros/lista_registros.html',
        {'registros': registros}
    )


# ======================================
# ESTADÍSTICAS
# ======================================


def estadisticas(request, habito_id):

    habito = get_object_or_404(
        HabitoBooleano,
        id=habito_id
    )

    porcentaje = AnalizadorHabitos.calcular_porcentaje(habito)

    racha = AnalizadorHabitos.calcular_racha_actual(habito)

    context = {
        'habito': habito,
        'porcentaje': porcentaje,
        'racha': racha
    }

    return render(
        request,
        'habitos/estadisticas.html',
        context
    )


def estadisticas_global(request):

    habitos = HabitoBooleano.objects.all()

    total = sum(
        AnalizadorHabitos.calcular_porcentaje(h)
        for h in habitos
    )

    return render(request, "habitos/estadisticas_global.html", {
        "total": total,
        "habitos": habitos
    })


# ======================================
# ELIMINAR HÁBITO
# ======================================


def eliminar_habito_booleano(request, habito_id):

    habito = get_object_or_404(
        HabitoBooleano,
        id=habito_id
    )

    if request.method == 'POST':

        habito.delete()

        return redirect('lista_habitos')

    return render(
        request,
        'habitos/eliminar_habito.html',
        {'habito': habito}
    )
