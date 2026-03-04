from django.urls import path
from .views import InstitutoListView, InstitutoDetailView

urlpatterns = [
    path('institutos/',          InstitutoListView.as_view(),   name='instituto-list'),
    path('institutos/<int:pk>/', InstitutoDetailView.as_view(), name='instituto-detail'),
    
]
