# Generic Tests
Bootstrap a functional testing suite. Arrives with Selenium WebDriver & Testful.API (a Selenium wrapper). 
Written in Python.

## Directory Structure
tba

## Dependencies
- pip 
 - pytest
 - selenium
 - virtualenv

- homebrew OPTIONAL
 - chromedriver OPTIONAL
 - phantomjs OPTIONAL

## Getting Started
### Install
If you do not have pip:
```sh
sudo easy_install pip
```

Install Virtual Env.:
```sh
sudo pip install virtualenv
```

Pull repository and setup Virtual Env.:
```sh
git clone https://github.com/alejandroq/TestfulBootstrap.git
virtualenv $ROOTDIR (def. TestfulBootstrap) 
```

Once Virtual Env. is Activated (next section):
```sh
pip install -r requirements.txt
```
OPTIONAL: 
To test on Chrome or Headless PhantomJS (as opposed to def. Firefox).
On a MacOS with Homebrew (no need to activate Virtual Env. for this):
```sh
brew install chromedriver
brew install phantomjs
```

### Activate Virtual Env.:
Activate Virtual Env. (or Python Container)
```sh
cd $ROOTDIR
source bin/activate
```

## Configuration:
```json
{
    "option 1" : "option 1 url",
    "option 2" : "option 2 url",

    "testing"  : "option 1",
    "browser"  : "chrome"
}

// TODO: enable cli args to allow for 
// for calls within cli browser options 
// (dependent upon above installations):
chrome, phantomjs and firefox
```
### How to:
"option 1":"option 1 url"

ex. "dev":"http://alexq.dev.me"

given ex. above - "testing":"dev", will set WebDriver to instantiate at "http://alexq.dev.me"

### Note: 
[PhantomJS](http://phantomjs.org/) is for Headless Functional Testing.

### Trello:
tba

## To Use:
To Run Tests (once Virtual Env is activated):
```sh
python $ROOTDIR/tests/main.py [optionals tba]
```

## Writing Tests:
tba

## Resources:
[py.test docs](http://doc.pytest.org/en/latest/contents.html)
[selenium python docs](http://selenium-python.readthedocs.io/)
