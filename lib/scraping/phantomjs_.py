
# -*- coding: utf-8 -*-

import sys,os
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
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
				self.log.warning("Caught TimeoutException at super().get(" + url + ")")
				self.log.warning("save_current_page to ../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", self.current_url) + ".html and png")
				self.log.warning(e, exc_info=True)
				self.save_current_page("../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", self.current_url) + ".html")
				self.save_current_page("../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", self.current_url) + ".png")
				self.log.warning("%s", e)
				self.execute_script("window.stop();")

		if retries == 0:
			self.log.error("PhantomJS caught ERROR RemoteDisconnected at get" + url)
			self.save_current_page("../../var/ss/get_error.html")
			self.save_current_page("../../var/ss/get_error.png")

		if tag_to_wait != "":
			self.wait_appearance_of_tag(by="xpath", tag=tag_to_wait, timeout=timeout)

	def wait_appearance_of_tag(self, by="xpath", tag="", warning_messages=True, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start. tag: " + tag)
		retries = 10
		while retries > 0:
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
				break
			except (RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, by, tag, warning_messages, e)
				self.reconnect(self.current_url)
				retries -= 1
				self.log.debug("retries -= 1. retries[" + str(retries) + "]")
			except (TimeoutException, NoSuchElementException) as e:
				self.save_error_messages_at(sys._getframe().f_code.co_name, by, tag, warning_messages, e)
				return False
		if retries == 0:
			self.log.error("wait error at " + sys._getframe().f_code.co_name)
			self.log.error("retries == 0. please check url: " + self.current_url)
			filename = "../../var/ss/error_atwait_appearance_of_tag_"+ re.sub(r"/|:|\?|\.", "", self.current_url)
			self.save_current_page(filename + ".html")
			self.save_current_page(filename + ".png")

		self.log.debug("tag appeared. wait_appearance_of_tag Finished.return True")
		return True


	def save_error_messages_at(self, method, by, tag, warning_messages, exception):
		self.log.warning("caught " + exception.__class__.__name__ + " at wait_appearance_of_tag. url[" + self.current_url + "]")
		self.log.warning("by[" + by + "], tag[" + tag + "]")
		if warning_messages:
			self.log.warning("save_current_page to ../../var/ss/" + exception.__class__.__name__ + re.sub(r"/|:|\?|\.", "", self.current_url) + ".html and png")
			self.log.warning(exception, exc_info=True)
			filename = "../../var/ss/" + exception.__class__.__name__ + re.sub(r"/|:|\?|\.", "", self.current_url)
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
