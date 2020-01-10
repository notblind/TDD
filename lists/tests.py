from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from .views import index

# Create your tests here.

class IndexTest(TestCase):
	'''тест домашней страницы'''

	def test_index_return_correct_html(self):
		'''тест:корневой url возвращает верный html'''
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'lists/index.html')

