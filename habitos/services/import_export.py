import json

from habitos.models import (
    HabitoBooleano,
    HabitoContador,
    HabitoSemanal
)


class ExportadorHabitos:

    @staticmethod
    def exportar_json():

        habitos = []

        # BOOLEANOS
        for h in HabitoBooleano.objects.all():

            habitos.append({
                "tipo": "booleano",
                "nombre": h.nombre,
                "descripcion": h.descripcion,
                "fecha_inicio": str(h.fecha_inicio),
                "activo": h.activo
            })

        # CONTADOR
        for h in HabitoContador.objects.all():

            habitos.append({
                "tipo": "contador",
                "nombre": h.nombre,
                "descripcion": h.descripcion,
                "fecha_inicio": str(h.fecha_inicio),
                "activo": h.activo,
                "objetivo_diario": h.objetivo_diario
            })

        # SEMANAL
        for h in HabitoSemanal.objects.all():

            habitos.append({
                "tipo": "semanal",
                "nombre": h.nombre,
                "descripcion": h.descripcion,
                "fecha_inicio": str(h.fecha_inicio),
                "activo": h.activo,
                "objetivo_semanal": h.objetivo_semanal
            })

        return json.dumps(habitos, indent=4)

    @staticmethod
    def importar_json(archivo):

        datos = json.load(archivo)

        for item in datos:

            tipo = item.get("tipo")

            if tipo == "booleano":

                HabitoBooleano.objects.create(
                    nombre=item["nombre"],
                    descripcion=item["descripcion"],
                    fecha_inicio=item["fecha_inicio"],
                    activo=item["activo"]
                )

            elif tipo == "contador":

                HabitoContador.objects.create(
                    nombre=item["nombre"],
                    descripcion=item["descripcion"],
                    fecha_inicio=item["fecha_inicio"],
                    activo=item["activo"],
                    objetivo_diario=item["objetivo_diario"]
                )

            elif tipo == "semanal":

                HabitoSemanal.objects.create(
                    nombre=item["nombre"],
                    descripcion=item["descripcion"],
                    fecha_inicio=item["fecha_inicio"],
                    activo=item["activo"],
                    objetivo_semanal=item["objetivo_semanal"]
                )