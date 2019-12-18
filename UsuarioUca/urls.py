from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views

from . import views
from .views import HomeView, ListaVotacionesView, CrearVotacionView, FAQView, EstadisticasVotacionSimpleView, \
    EstadisticasEleccionView, UsuarioUcaListView, UsuarioUcaUpdate, UsuarioUcaCreate, MyModelImportView, \
    UsuarioUcaExportView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name="home"),
    path('listadoUsuarios/', UsuarioUcaListView.as_view(), name='usuariouca_list'),
    path('editarusuario/<int:pk>', UsuarioUcaUpdate.as_view(), name='usuariouca_edit'),
    path('crearusuario/', UsuarioUcaCreate.as_view(), name='usuariouca_create'),
    path('listavotaciones/', ListaVotacionesView.as_view(), name="listavotaciones"),
    path('usuariouca/import/', MyModelImportView.as_view(), name='usuariouca_import'),
    path('usuariouca/export/', UsuarioUcaExportView.as_view(), name='usuariouca_export'),
    path('usuariouca/import/confirm/', MyModelImportView.as_view(confirm=True),
        name='usuariouca_import_confirm'),
    path('faq/', FAQView.as_view(), name="faq"),
    path('estadisticasVotacionSimple/', EstadisticasVotacionSimpleView.as_view(), name="estadisticasvotacionsimple"),
    path('estadisticasEleccion/', EstadisticasEleccionView.as_view(), name="estadisticaseleccion"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('logout/', views.logout_request, name="logout"),
    path('eliminarusuario/<int:pk>', views.erase_request, name="eliminar"),


]