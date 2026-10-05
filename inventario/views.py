from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Categoria, Producto

# ---------- Públicas ----------
def index(request):
    return render(request, 'inventario/index.html')

def catalogo(request):
    productos = Producto.objects.select_related('categoria')
    q = request.GET.get('q', '').strip()
    cat = request.GET.get('categoria', '')
    if q:
        productos = productos.filter(nombre__icontains=q)
    if cat:
        productos = productos.filter(categoria_id=cat)
    return render(request, 'inventario/catalogo.html', {
        'productos': productos,
        'categorias': Categoria.objects.all(),
        'q': q,
        'cat_sel': cat,
    })

# ---------- Privadas ----------
class ProductoListView(PermissionRequiredMixin, ListView):          # Read (tabla)
    model = Producto
    template_name = 'inventario/admin_panel.html'
    context_object_name = 'productos'
    permission_required = 'inventario.view_producto'

class ProductoDetailView(PermissionRequiredMixin, DetailView):      # Read (detalle)
    model = Producto
    template_name = 'inventario/producto_detail.html'
    permission_required = 'inventario.view_producto'

class ProductoCreateView(PermissionRequiredMixin, CreateView):      # Create
    model = Producto
    fields = ['nombre', 'categoria', 'precio', 'stock', 'sku', 'fecha_ingreso']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('admin_panel')
    permission_required = 'inventario.add_producto'

class ProductoUpdateView(PermissionRequiredMixin, UpdateView):      # Update
    model = Producto
    fields = ['nombre', 'categoria', 'precio', 'stock', 'sku', 'fecha_ingreso']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('admin_panel')
    permission_required = 'inventario.change_producto'

class ProductoDeleteView(PermissionRequiredMixin, DeleteView):      # Delete
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('admin_panel')
    permission_required = 'inventario.delete_producto'