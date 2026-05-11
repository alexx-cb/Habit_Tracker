from django.utils.timezone import now
from datetime import timedelta

class AnalizadorHabitos:

    @staticmethod
    def calcular_porcentaje(habito):

        registros = habito.registro.all()

        total = registros.count()

        if total == 0:
            return 0

        cumplidos = registros.filter(cumplido=True).count()

        return round((cumplidos / total) * 100, 2)


    @staticmethod
    def calcular_racha_actual(habito):
        registros = habito.registro.filter(cumplido=True).order_by('-fecha')

        if not registros.exists():
            return 0

        racha = 0

        fecha_actual = now().date()

        for registro in registros:
            if registro.fecha == fecha_actual:
                racha +=1
                fecha_actual -= timedelta(days=1)


            else:
                break

        return racha


    @staticmethod
    def calcular_total_cumplidos(habito):
        return habito.registro.filter(cumplido=True).count()
