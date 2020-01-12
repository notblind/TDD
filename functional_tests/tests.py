from django.test import LiveServerTestCase

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class NewUserSite(LiveServerTestCase):
	'''тест нового юзера'''

	MAX_WAIT = 10

	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()

	def tearDown(self):
		'''завершение'''
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		'''ожидание строки в таблице'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('list_table')
				rows = table.find_elements_by_tag_name('td')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.tine() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_start_list_and_retrieve_it(self):
		'''тест: начало заполнения списка и предоставлние его позже'''

		#Пользователь открывает гланвую страницу
		self.browser.get(self.live_server_url)

		#Пользователь видит в заголовке и шапке сайта название 'Список дел'
		self.assertIn('Список дел', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Список дел', header_text)
		

		#На странице сразу же располагается форма для ввода дела
		inputbox = self.browser.find_element_by_id('new_item')
		self.assertEqual('Новое дело', inputbox.get_attribute('placeholder'))

		#Вводит какаое-ниудь дело (купить хлеб)
		inputbox.send_keys('Купить хлеб')

		#Нажимает Enter
		#Страница обновляется и появлется надпись "купить хлеб"
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		self.wait_for_row_in_list_table('Купить хлеб')

		#Форма для ввода также присутвует
		inputbox = self.browser.find_element_by_id('new_item')

		#Пользователь вводит еще одно дело (полить цветы)
		inputbox.send_keys('Полить цветы')

		#Нажимает Enter
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		#Страница обновляется и выводится уже две строчки дел
		self.wait_for_row_in_list_table('Купить хлеб')
		self.wait_for_row_in_list_table('Полить цветы')

		#Пользователь хочет проверить, запомнит ли сайт ее дела при следующем входе на сайт
		#На сайте есть пояснение об url адресе
		#П нему список пользователя будет сохранен

		#Пользователь посещает url адрес и спсок дел остается

		#Пользователь покидает сайт
		self.fail('Закончить тест')
