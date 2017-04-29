
# -*- coding: utf-8 -*-

from selenium import webdriver
class Webdriver_(webdriver):
	def __init__(self):
		print("__init__")
		super()

"""
class Webdriver_(webdriver.Firefox, webdriver.Chrome, webdriver.Ie, webdriver.PhantomJS):
	def __init__(self, browser):
		if browser.lower() == "ie":
			webdriver.Ie.__init__(self)
		elif browser.lower() == "chrome":
			webdriver.Chrome.__init__(self)
		elif browser.lower() == "firefox":
			webdriver.Firefox.__init__(self)
		elif browser.lower() == "phantomjs":
			print("browser.lower() == phantomjs")
			webdriver.PhantomJS.__init__(self)
		else:
			print("type error at Webdriver_.__init__")
"""		