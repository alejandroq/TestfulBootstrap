
from collections import Counter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import os 
import re
import time
import json
import random
import datetime
import threading
	
class Core():
	# def __init__(self, thread_argument = ''):
	# 	self.thread_argument = thread_argument
	# 	print self.thread_argument

	def launch_chrome(self, website = '', wait_time = 1):
		self.browser = webdriver.Chrome()
		self.open(website)
		self.wait_time = wait_time
		print "Browser of choice is Chrome. \n"

	def launch_phantomjs(self, website = '', wait_time = 1):
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		self.open(website)
		self.wait_time = wait_time
		print "Browser of choice is PhantomJS. *Don't forget to pkill phantomjs afterwards!*\n"

	def launch_firefox(self, website = '', wait_time = 1):
		self.browser = webdriver.Firefox() 
		self.open(website)
		self.wait_time = wait_time
		print "Browser of choice is Firefox. \n"

	def open(self, website):
		if website is not '':
			self.browser.get(website)
		else: 
			print "No website to test declared!"

	def close(self):
		self.browser.quit()

	def read(self, meta, file_name = None, attribute = None):
		try: 
			with open(file_name) as data_file:
				data = json.load(data_file)
				return data[meta]
		except:
			if attribute is not None and attribute is not 'text' and attribute is not 'link_text':
				return str(meta.get_attribute(attribute)).upper()
			else: 
				return meta.text.upper().encode('utf-8')

	def compare(self, elem, expected, attribute = None):
		actual = str(self.read(elem, attribute = attribute))
		expected = str(expected).upper()
		
		if actual == expected:
			print '\tIt\'s a match in heaven (this was expected, right?)!\n'
		else: 
			print '\tThe expected value of', expected, \
			'does not match the element.\n \tIt could be a UNICODE to ASCII issue. Or you found a bug... \n' \
			'\tI read from the website, \'', actual, '\'. Your expected value was \'', expected,'\'.\n'
		
		self.compare_actual_value_of_thing_to_your_expected_value(actual, expected)

	def write(self, elem, value):
		elem.clear()
		elem.send_keys(value)

	def locate(self, data):
		location = data['identify_by']

		# can optimize
		# http://selenium-python.readthedocs.io/locating-elements.html?highlight=find%20elements
		# perhaps could utilize a mapping function to compute at C level

		# more efficient if/else
		# http://stackoverflow.com/questions/17166074/most-efficient-way-of-making-an-if-elif-elif-else-statement-when-the-else-is-don

		if location == 'html_id':
			return self.browser.find_element_by_id(data['thing'])
		elif location == 'html_name':
			return self.browser.find_element_by_name(data['thing'])
		elif location == 'partial_link_text':
			return self.browser.find_element_by_partial_link_text(data['thing'])
		elif location == 'link_text':
			return self.browser.find_element_by_link_text(data['thing'])
		elif location == 'css_selector':
			return self.browser.find_element_by_css_selector(data['thing'])
		elif location == 'x_path':
			return self.browser.find_element_by_xpath(data['thing'])
		elif location == 'current_url':
			return self.browser.current_url

	def print_xpath_name(self, data):
		# for instances of no text - could have it loop (name, etc) until finally returning xPath.

		string = data['thing']
		if data['identify_by'] == 'x_path':
			elem = self.locate(data)
			string = self.read(elem, attribute = 'text')
		return string

	def check_existance_of_form_elem_name(self, arr, field):
		x = []
		for a in arr:
			if a['name'] != '':
				x.append(a['name'])
		
		x = Counter(x)
		
		if x[field.get_attribute('name')] > 0:
			return True
		else:
			return False

	def populate_form(self, elem, solution):

		fields = elem.find_elements(By.CSS_SELECTOR, '*')
		arr = []

		for field in fields:
			# could re-write a lot of this better
			try:
				# not properly accomodating labels
				field_type = field.get_attribute('type').lower()

				if field_type == 'fieldset' or field_type == 'hidden':
					# break it
					x = 1/0

				if field_type != 'checkbox' and field_type != 'radio' and field_type != 'label':
					self.write(field, self.random_val(field.get_attribute('type')))
					arr.append(self.return_values(field))
					children = self.return_child_nodes(field)
					for child in children:
						arr.append(self.return_values(child))
				else:
					if self.check_existance_of_form_elem_name(arr, field) == False and field_type != 'checkbox':
						self.browser.execute_script("arguments[0].click()", field) 
						arr.append(self.return_values(field))
						children = self.return_child_nodes(field)
						for child in children:
							arr.append(self.return_values(child))

					elif bool(random.getrandbits(1)):
						if field_type == 'radio':
							arr.pop() 
						self.browser.execute_script("arguments[0].click()", field) 
						arr.append(self.return_values(field))
						children = self.return_child_nodes(field)
						for child in children:
							arr.append(self.return_values(child))
			except: 
				continue
		elem.submit()
		
		solution(arr)

	# for form thing *NEEDS FIXING*
	def return_values(self, elem):
		# elem_id = self.read(elem, attribute = 'id')
		# consider removing str() utf-8 issues
		res = {'id' : str(elem.get_attribute('id')), 'value' : str(elem.get_attribute('value')), \
		'type' : str(elem.get_attribute('type')), 'text' : str(elem.text), 'name' : str(elem.get_attribute('name'))}
		return res

	def return_child_nodes(self, elem):
		return elem.find_elements_by_css_selector('*') 

	# could use true randomization
	def random_val(self, elem_type):
		if elem_type.lower() == 'text'.lower():
			return '01-01-2000'
		elif elem_type.lower() == 'email'.lower():
			return 'random@gmail.com'

	def action(self, data):
		action = data['action']

		# free of location
		if action == 'open' or action == 'navigate_to':
			print "I am changing our voyage to", data['thing'], "\n"
			self.open(data['thing'])
		elif action == 'screenshot' or action == 'capture':
			self.capture()
		elif action == 'quit' or action == 'end' or action == 'close':
			self.close()
		else: 
			elem = self.locate(data)

		# location dependent
		if action == 'click':
			print "I clicked on", self.print_xpath_name(data),"on page",self.browser.current_url,"\n"
			self.browser.execute_script("arguments[0].click()", elem) 
		elif action == 'set' or action == 'write' or action == 'type' or action == 'insert':
			print "I am writing", data['write'], "on", data['thing'],"on page",self.browser.current_url,"\n"
			self.write(elem, data['write']) 
		elif action == 'complete_form':
			print "Spidering and completing selected Form."
			self.populate_form(elem, data['expected_value'])
		elif action == 'compare':
			exp = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
			result = exp.findall(data['thing'])
			if len(result) == 0:  
				# print "I am comparing", data['thing'], "on the page", self.browser.current_url, "to the expected value of:", data['expected_value']
				print "I am comparing", self.print_xpath_name(data), "on the page", self.browser.current_url, "to the expected value of:", data['expected_value']
			else:
				print "I am comparing the local url to the expected url of:", data['expected_value']
			
			attribute = None

			try:
				attribute = data['attribute']
			except:
				pass
			self.compare(elem, data['expected_value'], attribute)

		self.wait(self.wait_time) # make selectable from data.json or default at 1. 

	def sequence(self, actions, configuration = {}):
		if configuration:
			for action in actions:
				self.action(self.wrap(action, configuration))
		elif actions is not None:
			for action in actions:
				self.action(action)

		# perhaps derive a way to waive this specific requirement for sequence of sequences.
		return {'thing' : None, 'action' : None, 'identify_by' : None}
		
	def wrap(self, incomplete_action, configuration):
		complete_action = {}

		optionals = ['expected_value', 'write', 'attribute']
		for option in optionals:
			try:
				complete_action[option] = incomplete_action[option]
			except:
				continue

		settings = ['identify_by', 'action', 'thing']

		# test of removing necessity of keypair 'thing'
		if '' in incomplete_action.keys():
			incomplete_action['thing'] = incomplete_action['']
		elif 7 in incomplete_action.keys():
			incomplete_action['thing'] = incomplete_action[7]


		for setting in settings:
			try:
				complete_action[setting] = incomplete_action[setting]
			except:
				complete_action[setting] = configuration[setting]

		return complete_action

	def wait(self, seconds):
		time.sleep(seconds)

	def capture(self):
		directory = 'screenshots'
		if not os.path.exists(directory):
			os.makedirs(directory)

		temp = 'screenshots/Screenshot:{:%Y-%m-%d %H:%M:%S}'
		file_name = temp.format(datetime.datetime.now())

		self.browser.save_screenshot(file_name)

	# Default Configurations:
	click_of_xpaths = { 'identify_by' : 'x_path', 'action' : 'click' }
	click_of_html_ids = { 'identify_by' : 'html_id', 'action' : 'click' }
	click_of_html_names = { 'identify_by' : 'html_name', 'action' : 'click' }
	click_of_link_texts = { 'identify_by' : 'link_text', 'action' : 'click' }
	click_of_css = { 'identify_by' : 'css_selector', 'action' : 'click' }

	compare_xpaths = { 'identify_by' : 'x_path', 'action' : 'compare' }
	compare_html_ids = { 'identify_by' : 'html_id', 'action' : 'compare' }
	compare_html_names = { 'identify_by' : 'html_name', 'action' : 'compare' }
	compare_link_texts = { 'identify_by' : 'link_text', 'action' : 'compare' }
	compare_css = { 'identify_by' : 'css_selector', 'action' : 'compare' }

	write_xpaths = { 'identify_by' : 'x_path', 'action' : 'write' }
	write_html_ids = { 'identify_by' : 'html_id', 'action' : 'write' }
	write_html_names = { 'identify_by' : 'html_name', 'action' : 'write' }
	write_link_texts = { 'identify_by' : 'link_text', 'action' : 'write' }
	write_css = { 'identify_by' : 'css_selector', 'action' : 'write' }

	completion_of_form_by_xpaths = { 'identify_by' : 'x_path', 'action' : 'complete_form' }
	completion_of_form_by_html_ids = { 'identify_by' : 'html_id', 'action' : 'complete_form' }
	completion_of_form_by_html_names = { 'identify_by' : 'html_name', 'action' : 'complete_form' }
	completion_of_form_by_link_texts = { 'identify_by' : 'link_text', 'action' : 'complete_form' }
	completion_of_form_by_css = { 'identify_by' : 'css_selector', 'action' : 'complete_form' }

	def click_of_xpaths_for(self, things):
		self.sequence(things, self.click_of_xpaths)

	def click_of_html_ids_for(self, things):
		self.sequence(things, self.click_of_html_ids)

	def click_of_html_names_for(self, things):
		self.sequence(things, self.click_of_html_names)

	def click_of_link_texts_for(self, things):
		self.sequence(things, self.click_of_link_texts)

	def click_of_css_for(self, things):
		self.sequence(things, self.click_of_css)

	def compare_xpaths_for(self, things):
		self.sequence(things, self.compare_xpaths)

	def compare_html_ids_for(self, things):
		self.sequence(things, self.compare_html_ids)

	def compare_html_names_for(self, things):
		self.sequence(things, self.compare_html_names)

	def compare_link_texts_for(self, things):
		self.sequence(things, self.compare_link_texts)

	def compare_css_for(self, things):
		self.sequence(things, self.compare_css)

	def write_on_xpaths_for(self, things):
		self.sequence(things, self.write_xpaths)

	def write_on_html_ids_for(self, things):
		self.sequence(things, self.write_html_ids)

	def write_on_html_names_for(self, things):
		self.sequence(things, self.write_html_names)

	def write_on_link_texts_for(self, things):
		self.sequence(things, self.write_link_texts)

	def write_on_css_for(self, things):
		self.sequence(things, self.write_css)

	def completion_of_form_by_xpaths_for(self, things):
		self.sequence(things, self.completion_of_form_by_xpaths)

	def completion_of_form_by_html_ids_for(self, things):
		self.sequence(things, self.completion_of_form_by_html_ids)

	def completion_of_form_by_html_names_for(self, things):
		self.sequence(things, self.completion_of_form_by_html_names)

	def completion_of_form_by_link_texts_for(self, things):
		self.sequence(things, self.completion_of_form_by_link_texts)

	def completion_of_form_by_css_for(self, things):
		self.sequence(things, self.completion_of_form_by_css)

	def compare_actual_value_of_thing_to_your_expected_value(self, actual, expected):
		assert actual == expected
