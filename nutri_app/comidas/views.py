from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from comidas.models import Comida

class ComidaListView(ListView):
    model = Comida
    template_name = 'comidas/lista.html'

class ComidaDetailView(DetailView):
    model = Comida
    template_name = 'comidas/ficha.html'

class ComidaCreateView(CreateView):
    model = Comida
    fields = ['nombre', 'calorias']
    template_name = 'comidas/formulario.html'
    success_url = reverse_lazy('lista_comidas')

class ComidaUpdateView(UpdateView):
    model = Comida
    fields = ['nombre', 'calorias']
    template_name = 'comidas/formulario.html'
    success_url = reverse_lazy('lista_comidas')

class ComidaDeleteView(DeleteView):
    model = Comida
    template_name = 'comidas/confirmar_borrado.html'
    success_url = reverse_lazy('lista_comidas')

