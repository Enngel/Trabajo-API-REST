from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # RUTAS API (Formato Django / Sin Front-end)
    # ==========================================
    # Fíjate que hemos eliminado 'api/' del inicio
    path('institutos/', views.InstitutoListView.as_view(), name='lista_institutos'),
    path('institutos/<int:pk>/', views.InstitutoDetailView.as_view(), name='detalle_instituto'),
    path('institutos/<int:codigo>/ciclos/', views.CicloFormativoByInstitutoView.as_view(), name='ciclos_instituto'),

    # Si tienes rutas de ciclos formativos, añádelas aquí también sin el 'api/'
]