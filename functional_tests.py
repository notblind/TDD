from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys

class NewUserSite(unittest.TestCase):
	'''тест нового юзера'''

	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()

	def tearDown(self):
		'''завершение'''
		self.browser.quit()

	def test_start_list_and_retrieve_it(self):
		'''тест: начало заполнения списка и предоставлние его позже'''

		#Пользователь открывает гланвую страницу
		self.browser.get('http://localhost:8000')

		#Пользователь видит в заголовке и шапке сайта название 'Список дел'
		self.assertIn('Список дел', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('СПИСОК ДЕЛ', header_text)
		

		#На странице сразу же располагается форма для ввода дела
		inputbox = self.browser.find_element_by_id('new_item')
		self.assertEqual('Новое дело', inputbox.get_attribute('placeholder'))

		#Вводит какаое-ниудь дело (купить хлеб)
		inputbox.send_keys('Купить хлеб')

		#Нажимает Enter
		#Страница обновляется и появлется надпись "1. купить хлеб"
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		table = self.browser.find_element_by_id('list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text=='1: Купить хлеб' for row in rows),
			'Новый элемент не появился в таблице'
			)

		#Форма для ввода также присутвует

		#Пользователь вводит еще одно дело (полить цветы)
		#Нажимает на кнопку добавить
		#Страница обновляется и выводится уже две строчки дел

		#Пользователь хочет проверить, запомнит ли сайт ее дела при следующем входе на сайт
		#На сайте есть пояснение об url адресе
		#П нему список пользователя будет сохранен

		#Пользователь посещает url адрес и спсок дел остается

		#Пользователь покидает сайт
		self.fail('Закончить тест')

if __name__=='__main__':
	unittest.main(warnings='ignore')

