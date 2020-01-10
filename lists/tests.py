from django.test import TestCase
from django.urls import resolve
from .views import index

# Create your tests here.

class IndexTest(TestCase):
	'''тест домашней страницы'''

	def test_root_url_resolves_to_index_view(self):
		'''тест: корневой url преобразуется в представление домашней страницы'''

		found = resolve('/')
		self.assertEqual(found.func, index)