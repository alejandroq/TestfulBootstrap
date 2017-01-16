
import os
import sys
import pytest
import datetime

class Main(object):
	"""docstring for Main"""
	def __init__(self, arg):
		self.arg = arg

		if not os.path.exists('log'):
			os.makedirs('log')
		LOG = 'log/log_{:%Y-%m-%d_%H:%M:%S}.txt'.format(datetime.datetime.now())
		CALL = '--resultlog=%s tests.py' % (LOG)
		pytest.main(CALL)

# TODO: get cli arg to determine which url to test. 
# for now to determine in config: refer to url key 
# under "website"
if __name__ == "__main__":
    Main(sys.argv)