from django.contrib.auth.models import User
from django.db import models



class Usuario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
    )

    fecha_creacion = models.DateField(auto_now_add=True)

    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username


    def total_habitos(self)->int:
        """
        Devuelve el total de habitos del usuario
        :return: Int
        """
        return self.habitos.count()


    def total_registros(self)->int:
        """
        Devuelve el total de registros realizados
        :return: Int
        """
        return Registro.objects.filter(habito_usuario=self).count()

