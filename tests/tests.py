
from framework import Application

class Test(object):
	"""docstring for Test"""
	def setup(self):
		self.do = Application()

	def test_url(self):
		assert self.do.get_url() == 'http://alexq.me/'

	def teardown(self):
		self.do.testful.capture()
		self.do.quit()
