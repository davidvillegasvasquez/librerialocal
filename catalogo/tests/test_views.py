from django.test import TestCase

# Create your tests here.

from catalogo.models import Autor
from django.urls import reverse

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Crear 13 autores para pruebas de paginación
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Autor.objects.create(nombre='Christian %s' % author_num, apellido = 'Apellido %s' % author_num,)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalogo/autores/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('toditicosLosAutores'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('toditicosLosAutores'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'catalogo/autor_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('toditicosLosAutores'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['autor_list']) == 2)

    def test_lists_all_authors(self):
        #Obtenga la segunda página y confirme que tiene (exactamente) 3 elementos restantes
        resp = self.client.get(reverse('toditicosLosAutores')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['autor_list']) == 3)
