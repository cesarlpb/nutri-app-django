from django.test import TestCase
from django.urls import reverse
from comidas.models import Comida

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
        self.assertEqual(response.status_code, 302)  # Redirect after success
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

