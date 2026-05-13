import pandas as pd
from django.utils.timezone import now
from datetime import timedelta

from matplotlib import pyplot as plt


class AnalizadorHabitos:

    @staticmethod
    def calcular_porcentaje(habito):

        registros = habito.registros.all()

        total = registros.count()

        if total == 0:
            return 0

        cumplidos = registros.filter(cumplido=True).count()

        return round((cumplidos / total) * 100, 2)


    @staticmethod
    def calcular_racha_actual(habito):
        registros = habito.registros.filter(cumplido=True).order_by('-fecha')

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
        return habito.registros.filter(cumplido=True).count()


    @staticmethod
    def calcular_total_fallidos(habito):
        return habito.registros.filter(cumplido=False).count()


    @staticmethod
    def obtener_dataframe(habito):
        registros= habito.registros.all().values(
            "fecha",
            "cumplido",
            "valor"
        )

        df = pd.DataFrame(registros)
        return df


    @staticmethod
    def grafica_cumplimiento(habito):

        df = AnalizadorHabitos.obtener_dataframe(habito)

        if df.empty:
            print("No hay datos")
            return

        resumen = df["cumplido"].value_counts()


        plt.figure(figsize = (6,6))

        plt.pie(
            resumen,
            labels=["Cumplido", "Fallido"],
            autopct="%1.1f%%"
        )

        plt.title(f"Cumplimiento - {habito.nombre}")

        plt.show()


    @staticmethod
    def grafica_evolucion(habito):

        df = AnalizadorHabitos.obtener_dataframe(habito)

        if df.empty:
            print("No hay datos.")
            return

        df["fecha"] = pd.to_datetime(df["fecha"])

        diarios = df.groupby("fecha")["cumplido"].sum()

        plt.figure(figsize=(10, 5))

        plt.plot(
            diarios.index,
            diarios.values,
            marker="o"
        )

        plt.title(f"Evolución - {habito.nombre}")
        plt.xlabel("Fecha")
        plt.ylabel("Cumplimientos")

        plt.grid(True)

        plt.show()


    @staticmethod
    def grafica_barras(habito):

        df = AnalizadorHabitos.obtener_dataframe(habito)

        if df.empty:
            print("No hay datos.")
            return

        resumen = df["cumplido"].value_counts()

        plt.figure(figsize=(6, 5))

        plt.bar(
            ["Cumplidos", "Fallidos"],
            resumen.values
        )

        plt.title(f"Resumen - {habito.nombre}")

        plt.show()


    @staticmethod
    def grafica_valores(habito):

        df = AnalizadorHabitos.obtener_dataframe(habito)

        if df.empty or "valor" not in df:
            print("No hay valores numéricos.")
            return

        df["fecha"] = pd.to_datetime(df["fecha"])

        plt.figure(figsize=(10, 5))

        plt.plot(
            df["fecha"],
            df["valor"],
            marker="o"
        )

        plt.title(f"Valores registrados - {habito.nombre}")

        plt.xlabel("Fecha")
        plt.ylabel("Valor")

        plt.grid(True)

        plt.show()