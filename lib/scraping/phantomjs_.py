
# -*- coding: utf-8 -*-

##https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/phantomjs/webdriver.py

import sys,os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
from http.client import RemoteDisconnected

class PhantomJS_(webdriver.PhantomJS):
	def __init__(self, executable_path="",\
					port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,\
					service_args=None, service_log_path=None):
		self.executable_path = executable_path
		self.port = port
		self.PHANTOMJS = desired_capabilities
		self.service_args = service_args
		self.service_log_path = service_log_path
		
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
			

		if self.executable_path == "":
			self.executable_path = self.conf.getconf("phantomJS_pass")
		if self.service_args == None:
			self.service_args=["--webdriver-loglevel=DEBUG"]
		if self.service_log_path == None:
			self.service_log_path=self.conf.getconf("logdir") + self.conf.getconf("phantomjs_logfile")
		self.log.debug(__class__.__name__ + ".super().__init__ start")
		super().__init__(executable_path=self.executable_path, \
					port=self.port, desired_capabilities=self.PHANTOMJS, \
					service_args=self.service_args, service_log_path=self.service_log_path)

	
	def get(self, url, tag_to_wait="", by="xpath", timeout=30):
		retries = 10
		while retries > 0:
			try:
				self.log.debug("super().get(" + url + ") start")
				super().get(url)
				break
			except RemoteDisconnected as e:
				self.log.debug("PhantomJS caught RemoteDisconnected at get" + url)
				self.log.debug("%s", e)
				self.log.debug("retries[" + str(retries) + "]")
				super().__init__(executable_path=self.executable_path, \
						port=self.port, desired_capabilities=self.desired_capabilities, \
						service_args=self.service_args, service_log_path=self.service_log_path)
				retries -= 1
			except TimeoutException as e:
				self.log.warning("Caught TimeoutException at super().get(" + url + ") start")
				self.log.warning("%s", e)
				self.execute_script("window.stop();")
				
		if retries == 0:
			self.log.error("PhantomJS caught ERROR RemoteDisconnected at get" + url)
			self.save_current_page("./samples/get_error.html")
			self.save_current_page("./samples/get_error.png")
		
		if tag_to_wait != "":
			self.wait_appearance_of_tag(by="xpath", tag=tag_to_wait, timeout=timeout)

	def wait_appearance_of_tag(self, by="xpath", tag="", timeout=30):
		self.log.debug("wait_appearance_of_tag start. tag: " + tag)
		try:
			if by=="xpath":
				WebDriverWait(self, timeout).until(lambda self: self.find_element_by_xpath(tag))
			elif by=="css_selector":
				WebDriverWait(self, timeout).until(lambda self: self.find_element_by_css_selector(tag))
			elif by=="name":
				WebDriverWait(self, timeout).until(lambda self: self.find_element_by_name(tag))
			elif by=="tag_name":
				WebDriverWait(self, timeout).until(lambda self: self.find_element_by_tag_name(tag))
			else:
				self.log.waring("type error by=" + by + ", tag: " + tag)
		except TimeoutException as e:
			self.log.warning("caught TimeoutException at " + self.current_url)
			self.log.warning("by[" + by + "], tag[" + tag + "]")
			self.log.exception("%s", e)
		except NoSuchElementException as e:
			self.log.warning("caught NoSuchElementException at " + self.current_url)
			self.log.warning("by[" + by + "], tag[" + tag + "]")
			self.log.exception("%s", e)

		self.log.debug("wait_appearance_of_tag Finished.")
		
		
	def reconnect(self, url=""):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#session_id = self.session_id
		#webdriver.Remote(command_executor=url,desired_capabilities={})
		#self.session_id = session_id
		self.__init__(executable_path=self.executable_path,\
					port=self.port, desired_capabilities=self.PHANTOMJS,\
					service_args=self.service_args, service_log_path=self.service_log_path)
		self.get(url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

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