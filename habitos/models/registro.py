from django.core.exceptions import ValidationError
from django.db import models

from habitos.models.habito import Habito


class Registro(models.Model):
    habito = models.ForeignKey(
        "habitos.HabitoBooleano",
        on_delete=models.CASCADE,
        related_name="registros",
        blank=True,
        null=True,
    )

    habito_contador = models.ForeignKey(
        "habitos.HabitoContador",
        on_delete=models.CASCADE,
        related_name="registros",
        blank=True,
        null=True,
    )

    habito_semanal = models.ForeignKey(
        "habitos.HabitoSemanal",
        on_delete=models.CASCADE,
        related_name="registros",
        blank=True,
        null=True,
    )

    fecha = models.DateField()
    cumplido = models.BooleanField(default=False)

    valor = models.FloatField(
        blank=True,
        null=True,
    )

    notas = models.TextField(
        blank=True,
        null=True,
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Registro - {self.fecha}"


    def clean(self)->None:
        """
        Valida que el registro pertenezca unicamente a un tipo de hábito
        :return:None
        """

        relaciones = [
            self.habito,
            self.habito_contador,
            self.habito_semanal,
        ]

        relaciones_activas = sum(
            1 for r in relaciones if r is not None
        )

        if relaciones_activas !=1:
            raise ValidationError(
                "El registro debe pertenecer a un unico tipo de habito"
            )

    def obtener_habito(self)->Habito:
        """
        Devuelve el habito asociado independientemente de su tipo
        :return: Habito
        """

        return (
            self.habito or
            self.habito_contador or
            self.habito_semanal
        )

    def es_numerico(self):
        """
        Indica si el registro es numerico
        :return:
        """

        return self.valor is not None
