
# -*- coding: utf-8 -*-

import os
import sys
import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, StaleElementReferenceException
from http.client import RemoteDisconnected
from urllib.request import URLError

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log


class PhantomJS_(webdriver.PhantomJS):
	def __init__(self, executable_path="",\
					port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,\
					service_args=None, service_log_path=None):
		self.executable_path = executable_path
		self.port = port
		self.PHANTOMJS = desired_capabilities
		self.service_args = service_args
		self.service_log_path = service_log_path

		self.log = Log.getLogger()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		
		import logging, logging.handlers
		selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
		selenium_logger.setLevel(logging.ERROR)
		if len(selenium_logger.handlers) < 1:
			rfh = logging.handlers.RotatingFileHandler(
				filename=Conf.getconf("logdir")+Conf.getconf("phantomjs_logfile"),
				maxBytes=Conf.getconf("rotate_log_size"),
				backupCount=Conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			selenium_logger.addHandler(rfh)

			stream_handler = logging.StreamHandler()
			stream_handler.setFormatter(formatter)
			stream_handler.setLevel(Conf.getconf("loglevel_to_stdout"))
			selenium_logger.addHandler(stream_handler)
		

		if self.executable_path == "":
			self.executable_path = Conf.getconf("phantomJS_pass")
		if self.service_args == None:
			self.service_args=["--webdriver-loglevel=DEBUG"]
		if self.service_log_path == None:
			self.service_log_path=Conf.getconf("logdir") + Conf.getconf("phantomjs_logfile")
		self.log.debug(__class__.__name__ + ".super().__init__ start")
		super().__init__(executable_path=self.executable_path, \
					port=self.port, desired_capabilities=self.PHANTOMJS, \
					service_args=self.service_args, service_log_path=self.service_log_path)
		self.set_page_load_timeout(Conf.getconf("phantomJS_load_timeout"))


	def get(self, url, tag_to_wait="", by="xpath", timeout=30, warning_messages=True):
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
				self.save_error_messages_at(sys._getframe().f_code.co_name, "by[" + by + "], tag[" + tag_to_wait + "]", warning_messages, e, url=url)
				self.execute_script("window.stop();")

		if retries == 0:
			self.log.error("PhantomJS caught ERROR RemoteDisconnected at get" + url)
			self.save_current_page("../../var/ss/get_error.html")
			self.save_current_page("../../var/ss/get_error.png")

		if tag_to_wait != "":
			self.wait_appearance_of_tag(by=by, tag=tag_to_wait, timeout=timeout)


	def click(self, button):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		url = self.current_url
		retries = 10
		while retries > 0:
			try:
				button.click()
			except (NoSuchElementException, StaleElementReferenceException) as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, "click(button)", True, e)
				return False
			except (TimeoutException, RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.log.debug("caught " + e.__class__.__name__ + " at click(button). retries[" + str(retries) + "]")
				self.reconnect(url)
				time.sleep(Conf().getconf(
					"IEEE_wait_time_per_download_paper"))
				retries -= 1

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
		return True

	def find_element_with_handling_exceptions(self, by="XPATH", tag="", warning_messages=True, timeout=30, url=""):
		##By: CLASS_NAME, CSS_SELECTOR, ID, LINK_TEXT
		##, NAME, PARTIAL_LINK_TEXT,TAG_NAME, XPATH
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.log.debug("by: " + by + " , + tag: " + tag)
		retries = 10
		while retries > 0:
			try:
				element = self.find_element(eval("By." + by), tag)
				break
			except (NoSuchElementException, StaleElementReferenceException) as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, "by: " + by + ", tag: " + tag, True, e)
				raise e
			except (TimeoutException, RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.log.debug("caught " + e.__class__.__name__ + " at click(button). retries[" + str(retries) + "]")
				if url != "":
					self.reconnect(url)
				else:
					self.reconnect(self.current_url)
				time.sleep(Conf().getconf(
					"IEEE_wait_time_per_download_paper"))
				retries -= 1

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
		return element

	def wait_appearance_of_tag(self, by="xpath", tag="", warning_messages=True, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start. tag: " + tag)
		retries = 10
		while retries > 0:
			try:
				url = self.current_url
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
				break
			except (TimeoutException, RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, "by[" + by + "], tag[" + tag + "]", warning_messages, e, url=url)
				self.reconnect(self.current_url)
				retries -= 1
				self.log.debug("retries -= 1. retries[" + str(retries) + "]")
			except NoSuchElementException as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, "by[" + by + "], tag[" + tag + "]", warning_messages, e, url=url)
				return False
		if retries == 0:
			self.log.error("wait error at " + sys._getframe().f_code.co_name)
			self.log.error("retries == 0. please check url: " + self.current_url)
			filename = "../../var/ss/error_atwait_appearance_of_tag_"+ re.sub(r"/|:|\?|\.", "", self.current_url)
			self.save_current_page(filename + ".html")
			self.save_current_page(filename + ".png")

		self.log.debug("tag appeared. wait_appearance_of_tag Finished.return True")
		return True


	def save_error_messages_at(self, method, command, warning_messages, exception,  url=""):
		self.log.warning("caught " + exception.__class__.__name__ + " at " + method + ". url[" + url + "]")
		self.log.warning("command: " + command)
		if warning_messages:
			filename = "../../var/ss/" + exception.__class__.__name__ + re.sub(r"/|:|\?|\.", "", url)
			self.log.warning("save_current_page to " + filename + ".html and png")
			self.log.warning(exception, exc_info=True)
			self.save_current_page(filename + ".html")
			self.save_current_page(filename + ".png")
			self.log.debug("return False")


	def reconnect(self, url=""):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.__init__(executable_path=self.executable_path,\
					port=self.port, desired_capabilities=self.PHANTOMJS,\
					service_args=self.service_args, service_log_path=self.service_log_path)
		self.get(url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def execute_script_with_handling_exceptions(self, script):
		## script example
		## "window.scrollTo(0, document.body.scrollHeight);"
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("script: " + script)
		try:
			self.execute_script(script)
		except (RemoteDisconnected, ConnectionRefusedError, URLError) as e:
			self.save_error_messages_at(sys._getframe().f_code.co_name, script, warning_messages, e)
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
			self.log.error(__class__.__name__ + "." + sys._getframe().f_code.co_name)
			self.log.error("TYPEERROR suffix["+suffix+"]")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
