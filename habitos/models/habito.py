from datetime import timedelta

from django.db import models
from abc import ABC, abstractmethod


class Habito(models.Model, ABC):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-nombre']

    def __str__(self):
        return self.nombre

    @abstractmethod
    def es_cumplido_fecha(self, fecha)->bool:
        """
        Determina si un hábito se considera cumplido en una fecha correcta
        :param fecha: date con la fecha en el que se completa
        :return: bool
        """
        pass

    def calcular_progreso(self)->float:
        """
        Calcula el progreso que se lleva del hábito devolviendo un float con el porcetaje de cumplimiento
        :return: float
        """
    pass

class HabitoBooleano(Habito):


    def es_cumplido_fecha(self, fecha)->bool:
        return self.registros.filter(fecha=fecha, cumplido=True).exists()

    def calcular_progreso(self)->None:
        total = self.registros.count()

        if total == 0:
            return 0

        cumplidos = self.registros.filter(cumplido=True).count()
        return (cumplidos / total) * 100


class HabitoContador(Habito):

    objetivo_diario = models.IntegerField(default=1)

    def es_cumplido_fecha(self, fecha) ->bool:
        registro = self.registros.filter(fecha=fecha).first()

        if not registro:
            return False

        return registro.valor >= self.objetivo_diario

    def calcular_progreso(self)->float:
        registros = self.registros.all()
        if registros.count() == 0:
            return 0

        cumplidos = sum(1 for r in registros if r.valor >= self.objetivo_diario)
        return (cumplidos / registros.count()) * 100


class HabitoSemanal(Habito):

    objetivo_semanal = models.IntegerField(default=3)


    def es_cumplido_fecha(self, fecha) ->bool:
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        total = self.registros.filter(fecha_range=[inicio_semana, fin_semana], cumplido=True).count()

        return total >= self.objetivo_semanal


    def calcular_progreso(self)->float:
        registros = self.registros.filter(cumplido=True)

        if registros.count() == 0:
            return 0

        return min(100, (registros.count() / self.objetivo_semanal) * 100)