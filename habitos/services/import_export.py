import json
from datetime import datetime

from habitos.models import (
    HabitoBooleano,
    Registro
)


class ImportExportService:

    @staticmethod
    def exportar_habitos(habitos, ruta):

        datos = []

        for habito in habitos:

            datos.append({
                "nombre": habito.nombre,
                "descripcion": habito.descripcion,
                "fecha_inicio": str(habito.fecha_inicio),
                "activo": habito.activo
            })

        with open(ruta, "w", encoding="utf-8") as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def exportar_registros(registros, ruta):

        datos = []

        for registro in registros:

            datos.append({
                "fecha": str(registro.fecha),
                "cumplido": registro.cumplido,
                "valor": registro.valor,
                "notas": registro.notas
            })

        with open(ruta, "w", encoding="utf-8") as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def importar_habitos(ruta):

        with open(ruta, "r", encoding="utf-8") as archivo:

            datos = json.load(archivo)

        habitos_creados = []

        for item in datos:

            habito = HabitoBooleano.objects.create(
                nombre=item["nombre"],
                descripcion=item["descripcion"],
                fecha_inicio=datetime.strptime(
                    item["fecha_inicio"],
                    "%Y-%m-%d"
                ).date(),
                activo=item["activo"]
            )

            habitos_creados.append(habito)

        return habitos_creados