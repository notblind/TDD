from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from .views import index

# Create your tests here.

class IndexTest(TestCase):
	'''тест домашней страницы'''

	def test_root_url_resolves_to_index_view(self):
		'''тест: корневой url преобразуется в представление домашней страницы'''

		found = resolve('/')
		self.assertEqual(found.func, index)

	def test_index_return_correct_html(self):
		'''тест: домашняя страница возвращает верный html'''
		
		request = HttpRequest()
		response = index(request)
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>Список дел</title>', html)
		self.assertTrue(html.endswith('</html>'))