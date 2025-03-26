# 🥗 Proyecto Django: nutri_app - App de seguimiento nutricional

App de seguimiento nutricional con Django

---

## 📦 Estructura general

El proyecto contiene una app llamada `comidas` con soporte CRUD completo y templates que heredan de `base.html`:

```
nutri_app/ 
├── comidas/ 
├── templates/ 
│ ├── comidas/ 
  │ ├── base.html 
  │ ├── confirmar_borrado.html 
  │ ├── ficha.html 
  │ ├── formulario.html 
  │ └── lista.html
```

---

## ✅ 1. Crear proyecto y app

```bash
django-admin startproject nutri_app
cd nutri_app
python manage.py startapp comidas
```

## ✅ 2. Registrar la app en settings.py

```python
INSTALLED_APPS = [
    ...
    'comidas',
]
```

```python
# ...
LANGUAGE_CODE = 'es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True
```

## ✅ 3. Modelo: Comida

Archivo: comidas/models.py

```python
from django.db import models

class Comida(models.Model):
    nombre = models.CharField(max_length=100)
    calorias = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.calorias} kcal"
```

## ✅ 4. Migraciones


```bash
python manage.py makemigrations
python manage.py migrate
```

## ✅ 5. Crear vistas (CRUD)

**comidas/views.py**

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Comida

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
```

## ✅ 6. Crear URLs

**Archivo: **comidas/urls.py**

```python
from django.urls import path
from .views import ComidaListView, ComidaDetailView, ComidaCreateView, ComidaUpdateView, ComidaDeleteView

urlpatterns = [
    path('', ComidaListView.as_view(), name='lista_comidas'),
    path('comida/<int:pk>/', ComidaDetailView.as_view(), name='ficha_comida'),
    path('crear/', ComidaCreateView.as_view(), name='crear_comida'),
    path('editar/<int:pk>/', ComidaUpdateView.as_view(), name='editar_comida'),
    path('borrar/<int:pk>/', ComidaDeleteView.as_view(), name='borrar_comida'),
]
```

Y en `nutri_app/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comidas.urls')),
]
```

## ✅ 7. Templates (templates/comidas/)

**base.html**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Nutri App{% endblock %}</title>
</head>
<body>
    <header>
        <h1><a href="{% url 'lista_comidas' %}">Nutri App</a></h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**lista.html**

```html
{% extends 'comidas/base.html' %}
{% block title %}Lista de Comidas{% endblock %}
{% block content %}
<h2>Lista de Comidas</h2>
<a href="{% url 'crear_comida' %}">Añadir comida</a>
<ul>
{% for comida in object_list %}
    <li>
        <a href="{% url 'ficha_comida' comida.pk %}">{{ comida.nombre }}</a> - {{ comida.calorias }} kcal
        [<a href="{% url 'editar_comida' comida.pk %}">Editar</a>]
        [<a href="{% url 'borrar_comida' comida.pk %}">Borrar</a>]
    </li>
{% empty %}
    <li>No hay comidas registradas.</li>
{% endfor %}
</ul>
{% endblock %}
```

**ficha.html**

```html
{% extends 'comidas/base.html' %}
{% block title %}Ficha{% endblock %}
{% block content %}
<h2>{{ object.nombre }}</h2>
<p>Calorías: {{ object.calorias }}</p>
<p>Fecha: {{ object.fecha|date:"l d F Y" }}</p>
<a href="{% url 'lista_comidas' %}">Volver</a>
{% endblock %}
```

**formulario.html**

```html
{% extends 'comidas/base.html' %}
{% block title %}Formulario{% endblock %}
{% block content %}
<h2>Formulario</h2>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Guardar</button>
</form>
<a href="{% url 'lista_comidas' %}">Volver</a>
{% endblock %}
```

**confirmar_borrado.html**

```html
{% extends 'comidas/base.html' %}
{% block title %}Confirmar borrado{% endblock %}
{% block content %}
<h2>¿Borrar comida?</h2>
<p>¿Estás seguro de que quieres borrar "{{ object }}"?</p>
<form method="post">{% csrf_token %}
    <button type="submit">Sí, borrar</button>
</form>
<a href="{% url 'lista_comidas' %}">Cancelar</a>
{% endblock %}
```

## ✅ 8. Testing (en rama develop)

```bash
git checkout -b dev
```
**comidas/tests.py**

```python
from django.test import TestCase
from django.urls import reverse
from .models import Comida

class ComidaTests(TestCase):
    def setUp(self):
        self.comida = Comida.objects.create(nombre="Manzana", calorias=95)

    def test_lista_comidas(self):
        response = self.client.get(reverse('lista_comidas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manzana")

    def test_crear_comida(self):
        response = self.client.post(reverse('crear_comida'), {
            'nombre': 'Plátano',
            'calorias': 110
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comida.objects.count(), 2)

    def test_editar_comida(self):
        response = self.client.post(reverse('editar_comida', args=[self.comida.pk]), {
            'nombre': 'Manzana Roja',
            'calorias': 100
        })
        self.assertEqual(response.status_code, 302)
        self.comida.refresh_from_db()
        self.assertEqual(self.comida.nombre, 'Manzana Roja')

    def test_borrar_comida(self):
        response = self.client.post(reverse('borrar_comida', args=[self.comida.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comida.objects.count(), 0)
```

Para ejecutar los tests:

```bash
python manage.py test comidas
```

📝 Notas adicionales

- Asegúrate de tener configurado `TEMPLATES` correctamente en `settings.py`.

- Puedes extender `base.html` en cualquier otro template.

- Si la fecha aún aparece en inglés, activa manualmente el idioma en la vista usando translation.activate('es').

## TODO

- Añadir estilos de branding (logo, colores, fuentes, etc.)
- Formatear fichas de comidas en componentes de estilo `cards` a modo galería o grid o masonry (https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Masonry_layout)
- Extender modelo `Comida` para guardar información de composición nutricional
- Proteger rutas del CRUD con login (el usuario debe iniciar sesión antes)
- Añadir modelo(s) a panel admin para editarlo(s)

Good coding 🤠