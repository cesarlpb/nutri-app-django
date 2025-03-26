from django.urls import path
from .views import (
                    ComidaListView, 
                    ComidaDetailView, 
                    ComidaCreateView, 
                    ComidaUpdateView, 
                    ComidaDeleteView
                   )

urlpatterns = [
    path('', ComidaListView.as_view(), name='lista_comidas'),
    path('comida/<int:pk>/', ComidaDetailView.as_view(), name='ficha_comida'),
    path('crear/', ComidaCreateView.as_view(), name='crear_comida'),
    path('editar/<int:pk>/', ComidaUpdateView.as_view(), name='editar_comida'),
    path('borrar/<int:pk>/', ComidaDeleteView.as_view(), name='borrar_comida'),
]
