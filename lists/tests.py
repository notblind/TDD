from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from .views import index
from .models import Item

# Create your tests here.

class ListViewTest(TestCase):
	'''тест представления списка'''

	def test_user_list_template(self):
		'''тест: используется шаблон спсика'''
		response = self.client.get('/lists/el/')
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_displays_all_list_items(self):
		'''тест: отображаются все эелемнты списка'''
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')

		response = self.client.get('/lists/el/')

		self.assertContains(response, 'item 1')
		self.assertContains(response, 'item 2')


class IndexTest(TestCase):
	'''тест домашней страницы'''

	def test_index_return_correct_html(self):
		'''тест:корневой url возвращает верный html'''
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'lists/index.html')

	def test_can_save_a_POST_request(self):
		'''тест: можно сохранить post-запрос '''
		response = self.client.post('/', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirect_after_POST(self):
		'''тест: переадресует после post-запроса'''
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/el/')

	def test_saving_and_retrieving_item(self):
		'''тест: сохранение и получение элементов списка'''
		first_item = Item()
		first_item.text = 'The first list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'The second list item'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first list item')
		self.assertEqual(second_saved_item.text, 'The second list item')

	def test_only_saves_items_when_necessary(self):
		'''тест: сохраняет элементы, только когда нужно'''
		self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)



