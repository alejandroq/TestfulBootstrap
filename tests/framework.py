
from setup import Setup

class Application(object):
    """docstring for Application"""
    def __init__(self):
        setup = Setup()
        
        # testful api selenium wrapper
        # doc. tba.
        # @var Core self.testful
        self.testful = setup.testful

        # more traditional selenium exp. 
        # doc. in README.md Resources.
        # @var WebDriver self.driver
        self.driver  = self.testful.browser

    def get_url(self):
        return self.driver.current_url

    def quit(self):
        self.driver.quit()
