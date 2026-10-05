from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from inventario.models import Categoria, Producto

CATEGORIAS = {
    'Notebooks': 'Computadores portátiles para trabajo y estudio',
    'Smartphones': 'Teléfonos móviles de distintas gamas',
    'Periféricos': 'Mouse, teclados y audífonos',
    'Redes': 'Routers, switches y accesorios de conectividad',
    'Almacenamiento': 'Discos SSD, pendrives y tarjetas de memoria',
    'Monitores': 'Pantallas para oficina y gaming',
}

PRODUCTOS = [
    ('Notebook Lenovo IdeaPad 15 i5 16GB', 'Notebooks', '549990', 14, 'NB-LEN-001', 40),
    ('Notebook HP Pavilion 14 Ryzen 5', 'Notebooks', '489990', 9, 'NB-HP-002', 25),
    ('Notebook ASUS Vivobook 15 i7', 'Notebooks', '699990', 6, 'NB-ASU-003', 10),
    ('Samsung Galaxy A55 128GB', 'Smartphones', '349990', 25, 'SP-SAM-001', 30),
    ('Xiaomi Redmi Note 13 256GB', 'Smartphones', '229990', 30, 'SP-XIA-002', 18),
    ('Mouse Logitech M170 Inalámbrico', 'Periféricos', '9990', 80, 'PF-LOG-001', 60),
    ('Teclado Mecánico Redragon Kumara', 'Periféricos', '34990', 22, 'PF-RED-002', 35),
    ('Audífonos HyperX Cloud Stinger', 'Periféricos', '39990', 0, 'PF-HYP-003', 50),
    ('Router TP-Link Archer C6 AC1200', 'Redes', '32990', 18, 'RD-TPL-001', 22),
    ('Switch TP-Link 8 Puertos Gigabit', 'Redes', '21990', 12, 'RD-TPL-002', 15),
    ('SSD Kingston NV2 1TB NVMe', 'Almacenamiento', '64990', 40, 'AL-KIN-001', 12),
    ('Pendrive SanDisk 64GB USB 3.0', 'Almacenamiento', '7990', 100, 'AL-SAN-002', 45),
    ('Monitor LG 24" Full HD IPS', 'Monitores', '119990', 11, 'MN-LG-001', 8),
    ('Monitor Samsung 27" Curvo', 'Monitores', '169990', 5, 'MN-SAM-002', 3),
]

class Command(BaseCommand):
    help = 'Carga categorías y productos de prueba'

    def handle(self, *args, **options):
        categorias = {}
        for nombre, desc in CATEGORIAS.items():
            cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            categorias[nombre] = cat

        hoy = timezone.localdate()
        for nombre, cat, precio, stock, sku, dias in PRODUCTOS:
            Producto.objects.update_or_create(
                sku=sku,
                defaults={
                    'nombre': nombre,
                    'categoria': categorias[cat],
                    'precio': Decimal(precio),
                    'stock': stock,
                    'fecha_ingreso': hoy - timedelta(days=dias),
                },
            )
        self.stdout.write(self.style.SUCCESS(f'{len(CATEGORIAS)} categorías y {len(PRODUCTOS)} productos cargados'))