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
				if time.time() - start_time > NewUserSite.MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_start_list_for_one_user(self):
		'''тест: начало заполнения списка для одного пользователя'''

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
		#Пользователь покидает сайт


	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''тест: многочтсленнве пользователи могут начать списки по разным url'''

		#Пользователь #1 начинает новый список
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('new_item')
		inputbox.send_keys('Купить молоко')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('Купить молоко')

		#Пользователь #1 замечает, что список имеет уникальный URL
		user_first_list_url = self.browser.current_url
		self.assertRegex(user_first_list_url, '/lists/.+')

		#Пришел пользователь #2
		#Используем новый сеанс браузера, тем самым обеспечивая, чтобы
		#никакая информация от пользователя #1 не прошла через данные cookie и пр.

		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Пользователь #2 посещает домашнюю страницу. Списка пользователя #1 нет.
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить молоко', page_text) 

		#Пользователь #2 начинает новый список, вводя новый элемент.
		inputbox = self.browser.find_element_by_id('new_item')
		inputbox.send_keys('Хорошенько отдохнуть')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('Хорошенько отдохнуть')

		#Пользователь #2 получает уникальный URL
		user_second_list_url = self.browser.current_url
		self.assertRegex(user_second_list_url, '/lists/.+')
		self.assertNotEqual(user_second_list_url, user_first_list_url)

		#Дополнительная проверка на отсутствие данных от пользователя #1
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить молоко', page_text)
		self.assertIn('Хорошенько отдохнуть', page_text)

		#Оба пользователя покидают сайт