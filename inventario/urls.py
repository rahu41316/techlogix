from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('panel/', views.ProductoListView.as_view(), name='admin_panel'),
    path('panel/producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('panel/producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('panel/producto/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('panel/producto/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
]