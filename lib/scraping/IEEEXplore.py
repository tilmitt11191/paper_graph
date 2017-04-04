
# -*- coding: utf-8 -*-
import sys, os

class IEEEXplore:
	def __init__(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		
		self.opt = Search_options()
		self.log.debug("class " + __class__.__name__ + " created.")

	
	def get_papers_of_new_conferences(self, conference_num):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + "(conference_num=" + str(conference_num) + ") start.")
		
		
	def get_papers_by_keywords(self, keywords, num_of_papers):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info("keywords[" + keywords + "], num_of_papers[" + str(num_of_papers) +"]")

		driver = self.create_driver()
		self.set_keywords(driver, keywords)
		#self.print_h2_attributes(driver)
		#self.save_current_page(driver, filename="../../tmp/output/output.png")
		#self.save_current_page(driver, filename="../../tmp/output/output.html")
		
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		

	def get_papers_of_conference(self, conference_name):
		pass
	

	def create_driver(self, top_page=""):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")		
		from conf import Conf
		phantomjs_path = Conf.getconf("phantomJS_pass")
		if top_page == "":
			top_page = Conf.getconf("IEEE_top_page")
		from selenium import webdriver
		driver = webdriver.PhantomJS(phantomjs_path)
		self.log.debug("driver.get(" + top_page + ")")
		driver.get(top_page)
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return driver")
		return driver


	def set_keywords(self, driver, keywords):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		try:
			driver.find_element_by_name('queryText').send_keys(keywords)
			driver.find_element_by_class_name('Search-submit').click()
		except(Exception) as e:
			self.log.exception('[[EXCEPTON OCCURED]]: %s', e)
			sys.exit("[[EXCEPTON OCCURED]]please check logfile.")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	

	def set_options(self):
		pass
	
	
	def download_papers(self, driver, path, download_num=25):
		# 0:デスクトップ、1:システム規定のフォルファ、2:ユーザ定義フォルダ
		#driver.setPreference("browser.download.folderList",2)
		# 上記で2を選択したのでファイルのダウンロード場所を指定
		#driver.setPreference("browser.download.dir", path)
		# ダウンロード完了時にダウンロードマネージャウィンドウを表示するかどうかを示す真偽値。
		#driver.setPreference("browser.download.manager.showWhenStarting",False)
		links = driver.find_elements_by_class_name("pure-u-22-24")
		self.log.debug("len(links)[" + str(len(links)) + "]")
		i = 0
		for link in links:
			self.log.debug("txt:"+link.text)
			element = link.find_element_by_css_selector("h2 > a")
			pdf_title = element.text
			self.log.debug("pdf_title:"+pdf_title)
			pdf_url = self.convert_path_to_url(element.get_attribute("href"))
			self.log.debug("pdf_dir:"+pdf_url)
			
			element = link.find_element_by_css_selector("p")
			pdf_authors = link.find_element_by_css_selector("p").text.split("; ")
			self.log.debug("pdf_author:" + str(pdf_authors))
			
			print("pdf_title:"+pdf_title)
			print("pdf_dir:"+pdf_url)
			print("pdf_author:" + str(pdf_authors))
			
			i+=1
			if i >= download_num:
				self.log.debug("i>="+str(download_num)+"."+__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
				return 0
		self.log.debug("len(link)<"+str(download_num)+"."+__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
		return 0
		
	
	def convert_path_to_url(self, path):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start. path[" + path + "]")
		elements = path.split("/")
		number = elements[len(elements)-2]
		url = "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=" + str(number)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return " + url)
		return url
		
	
	## for debug
	def print_h2_attributes(self, driver):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		links = driver.find_elements_by_tag_name("h2")
		for link in links:
			print(link.text)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		
		
	def save_current_page(self, driver, filename):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		path, suffix=os.path.splitext(filename)
		self.log.debug("path["+path+"], suffix["+suffix+"]")
		if suffix==".html":
			f = open(filename, 'w')
			f.write(driver.page_source)
			f.close()
		elif suffix==".png":
			driver.save_screenshot(filename)
		else:
			self.log.error("TYPEERROR suffix["+suffix+"]")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		
	def show_options(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.opt.show_options()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

		

class Search_options:
	opts = {"show" : "All Results",
	        "PerPage" : "25",
	        "SortBy" : "MostCited[ByPapers]",
	        "ContentType" : "None",
	        "YearType" : "Range",
	        "YearFrom" : "2015",
	        "YearTo" : "2017",
	        "Year" : "2017",
	        "Author" : "None",
	        "Affiliation" : "None",
	        "PublicationTitle" : "None",
	        "Publisher" : "None",
	        "ConferenceLocation" : "None",
	        }
	
	def __init__(self):
		import sys,os
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		
		self.log.debug("class " + __class__.__name__ + " created.")
	
	def show_options(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		for key, value in self.opts.items():
			print(key + "[" +value +"]")
	
	
	
	