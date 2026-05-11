from datetime import date
from django.core.exceptions import ValidationError

from habitos.models import (
    HabitoBooleano,
    HabitoContador,
    HabitoSemanal,
    Registro
)

class GestorHabitos:

    """
    ------------------
    CREADOR REGISTROS
    -----------------
    """

    @staticmethod
    def registrar_booleano(habito: HabitoBooleano, fecha: date, cumplido: bool):
        """
        Registra un hábito tipo booleano (sí/no).
        """

        if Registro.objects.filter(habito=habito, fecha=fecha).exists():
            raise ValidationError("Ya existe un registro para esta fecha.")

        return Registro.objects.create(
            habito=habito,
            fecha=fecha,
            cumplido=cumplido
        )

    @staticmethod
    def registrar_contador(habito: HabitoContador, fecha: date, valor: float):
        """
        Registra un hábito basado en cantidad (ej: minutos, páginas).
        """

        if Registro.objects.filter(habito=habito, fecha=fecha).exists():
            raise ValidationError("Ya existe un registro para esta fecha.")

        cumplido = valor >= habito.objetivo_diario

        return Registro.objects.create(
            habito=habito,
            fecha=fecha,
            valor=valor,
            cumplido=cumplido
        )


    @staticmethod
    def registrar_semanal(habito: HabitoSemanal, fecha: date, cumplido: bool):
        """
        Registro simple para hábitos semanales.
        """

        return Registro.objects.create(
            habito=habito,
            fecha=fecha,
            cumplido=cumplido
        )


    """
    --------------------
    FUNCIONALIDAD EXTRA
    --------------------
    """

    @staticmethod
    def marcar_como_cumplido(registro: Registro):
        """
        Marca un registro existente como cumplido.
        """

        registro.cumplido = True
        registro.save()


    @staticmethod
    def eliminar_registro(registro: Registro):
        """
        Elimina un registro.
        """

        registro.delete()


    @staticmethod
    def obtener_registros_habito(habito):
        """
        Devuelve todos los registros de un hábito ordenados.
        """

        return habito.registros.all().order_by("-fecha")


    @staticmethod
    def duplicar_dia_anterior(habito, fecha: date):
        """
        Copia el valor del día anterior (útil para hábitos continuos).
        """

        anterior = habito.registros.filter(
            fecha__lt=fecha
        ).order_by("-fecha").first()

        if not anterior:
            return None

        return Registro.objects.create(
            habito=habito,
            fecha=fecha,
            cumplido=anterior.cumplido,
            valor=getattr(anterior, "valor", None)
        )