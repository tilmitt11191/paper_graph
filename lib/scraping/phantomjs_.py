
# -*- coding: utf-8 -*-

##https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/phantomjs/webdriver.py

import sys,os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class PhantomJS_(webdriver.PhantomJS):
	def __init__(self, executable_path="",\
					port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,\
					service_args=None, service_log_path=None):

		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from conf import Conf
		self.conf = Conf()
		from log import Log as l
		self.log = l.getLogger()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		
		import logging, logging.handlers
		selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
		selenium_logger.setLevel(logging.ERROR)
		if len(selenium_logger.handlers) < 1:
			rfh = logging.handlers.RotatingFileHandler(
				filename=self.conf.getconf("logdir")+self.conf.getconf("logfile"),
				maxBytes=self.conf.getconf("rotate_log_size"), 
				backupCount=self.conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			selenium_logger.addHandler(rfh)
			
			stream_handler = logging.StreamHandler()
			stream_handler.setFormatter(formatter)
			stream_handler.setLevel(self.conf.getconf("loglevel_to_stdout"))
			selenium_logger.addHandler(stream_handler)
			

		if executable_path == "":
			executable_path = self.conf.getconf("phantomJS_pass")
		if service_args == None:
			service_args=["--webdriver-loglevel=ERROR"]
		if service_log_path == None:
			service_log_path=self.conf.getconf("logdir") + self.conf.getconf("phantomjs_logfile")
		self.log.debug(__class__.__name__ + ".super() start")
		super().__init__(executable_path=executable_path, \
					port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,\
					service_args=service_args, service_log_path=service_log_path)



	def save_current_page(self, filename):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		path, suffix=os.path.splitext(filename)
		self.log.debug("path["+path+"], suffix["+suffix+"]")
		if suffix==".html":
			f = open(filename, 'w')
			f.write(self.page_source)
			f.close()
		elif suffix==".png":
			self.save_screenshot(filename)
		else:
			self.log.error("TYPEERROR suffix["+suffix+"]")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


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