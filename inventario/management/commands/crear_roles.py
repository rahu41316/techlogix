from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from inventario.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Crea grupos, permisos y usuarios de prueba'

    def handle(self, *args, **options):
        g_admin, _ = Group.objects.get_or_create(name='Administrador')
        g_asist, _ = Group.objects.get_or_create(name='Asistente')

        for modelo in (Producto, Categoria):
            ct = ContentType.objects.get_for_model(modelo)
            perms = Permission.objects.filter(content_type=ct)
            g_admin.permissions.add(*perms)                                  # add, change, delete, view
            g_asist.permissions.add(*perms.filter(codename__startswith='view_'))  # solo lectura

        usuarios = [
            ('admin_tech', 'Admin2026!', g_admin),
            ('asistente_tech', 'Asistente2026!', g_asist),
        ]
        for username, clave, grupo in usuarios:
            user, _ = User.objects.get_or_create(username=username)
            user.is_staff = True          # necesario para entrar a /admin
            user.set_password(clave)
            user.save()
            user.groups.set([grupo])

        self.stdout.write(self.style.SUCCESS('Roles y usuarios creados'))