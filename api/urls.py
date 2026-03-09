from django.urls import path
from . import views

urlpatterns = [
    # Ruta para ver la lista completa de institutos y poder buscar/filtrar
    path('institutos/', views.InstitutoListView.as_view(), name='lista_institutos'),

    # Ruta para ver el detalle de un solo instituto (usando su ID o primary key 'pk')
    path('institutos/<int:pk>/', views.InstitutoDetailView.as_view(), name='detalle_instituto'),
]