
import json
from testful import Core

class Setup(object):
    """docstring for Setup"""
    def __init__(self):
        with open('config.json') as config:
            self.drive(json.load(config))

    def drive(self, json):
        # TODO: config to determine which browser launch
        self.testful      = Core()
        browser      = json['browser']
        if   'ch' in browser:
            self.testful.launch_chrome(json[json['testing']])
        elif 'fi' in browser:
            self.testful.launch_firefox(json[json['testing']])
        elif 'ph' in browser: 
            self.testful.launch_phantomjs(json[json['testing']])