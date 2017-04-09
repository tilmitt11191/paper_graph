
# -*- coding: utf-8 -*-
import sys, os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


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
		self.search_by_keywords(driver, keywords)
		urls = self.get_urls_of_papers(driver, num_of_papers)
		for url in urls:
			driver.get(url)
			paper_attributes, citing_urls, cited_urls = self.get_attributes_and_download_pdf(driver)
		
		
		#self.print_h2_attributes(driver)
		#self.save_current_page(driver, filename="../../tmp/output/output.png")
		#self.save_current_page(driver, filename="../../tmp/output/output.html")
		
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		

	def get_papers_of_target_conference(self, conference_name):
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


	def search_by_keywords(self, driver, keywords):
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
		
		
	
	def get_urls_of_papers(self, driver, num_of_papers):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		urls = []
		links = driver.find_elements_by_class_name("pure-u-22-24")
		self.log.debug("len(links)[" + str(len(links)) + "]")

		for link in links:
			element = link.find_element_by_css_selector("h2 > a")
			urls.append(element.get_attribute("href"))

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return " + str(urls))
		return urls
	
	
	def get_attributes_and_download_pdf(self, url, driver):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		import table_papers
		paper = table_papers.Table_papers()
		
		##title
		#element = driver.find_element_by_tag_name("title")
		#element = driver.find_element_by_id("title")
		#element = driver.find_element_by_css_selector("html > title")
		#element = driver.find_element_by_class_name("title")
		paper.title = driver.title
		
		
		##authors
		#<span ng-bind-html="::author.name" class="ng-binding">
		#elements = driver.find_elements_by_class_name("authors-container")
		#print(str(len(elements)))
		elements = driver.find_elements_by_xpath('//span[@ng-bind-html="::author.name"]')
		#print(str(len(elements))) #5
		for el in elements:
			paper.authors += ","+el.text
		paper.authors = paper.authors[1:]
		
		
		##keywords
		elements = driver.find_elements_by_xpath('//a[@ng-bind-html="::term"]')
		#print(str(len(elements))) #21
		for el in elements:
			keyword = el.text
			if keyword in paper.keywords:
				self.log.debug("keyword[" + keyword + "] is deplicated. not add.")
			else:
				paper.keywords += ","+el.text
		paper.keywords = paper.keywords[1:]
		
		
		##citing_papers
		##citing_urls
		"""
					<a ng-href="/document/4116687" title="Usilng Machine Learning Technliques to Identify Botnet Traffic" target="_self" href="/document/4116687">
				<span ng-bind-html="::(vm.contextData.isStandard ? article.standardNumber + ' - ' + article.title : article.title) | charlimitHtml:185" mathjax-bind="" class="ng-binding">Usilng Machine Learning Technliques to Identify Botnet Traffic</span>
			</a>
			<div class="ng-binding">Carl Livadas; Robert Walsh; David Lapsley; W. Timothy Strayer</div>
		</div><!-- end ngRepeat: article in vm.contextData.similar --><div class="doc-all-related-articles-list-item ng-scope" ng-repeat="article in vm.contextData.similar"> 
		"""
		citing_papers = []
		citing_urls = []
		#elements = driver.find_elements_by_xpath('//h2[@class="document-ft-section-header"]/a')
		elements = driver.find_element_by_xpath('//div[@class="stats-document-relatedArticles ng-scope"]')\
							.find_elements_by_tag_name('a')
		#print(element.text)
		#elements = element.find_elements_by_xpath('/a')
		#print(str(len(elements))) #10
		for el in elements:
			citing_url = el.get_attribute("href")
			citing_paper = table_papers.Table_papers(title=el.get_attribute("title"), url=citing_url)
			citing_paper.insert()
			paper.citings += "," + str(citing_paper.id)
			citing_papers.append(citing_paper)
			citing_urls.append(citing_url)
			citing_paper.insert()
		paper.citings = paper.citings[1:]


		##conference
		conference = driver.find_element_by_xpath('//div[@class="u-pb-1 stats-document-abstract-doi ng-scope"]')\
							.find_element_by_tag_name('a').text

		paper.conference = conference
		
		#Date of Publication: 06 January 200 or Date of Conference 14-16 Nov. 2006
		try:
			date = driver.find_element_by_xpath('//div[@ng-if="::vm.details.isConference == true"]').text
		except NoSuchElementException:
			self.log.debug("catch NoSuchElementException. date = ''") ##todo paper
			date = ""
		paper.published = self.convert_to_datetime(date)
		
		##url
		paper.url = url
		
		##timestamp
		import time
		paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

		##path

		##cited_papers
		##cited_urls
		#href="/document/4116687/citations?tabFilter=papers"
		#http://ieeexplore.ieee.org/document/4116687/citations?anchor=anchor-paper-citations-ieee&ctx=citations
		
		"""
		try:
			driver.find_element_by_name('queryText').send_keys(keywords)
			driver.find_element_by_class_name('Search-submit').click()
		except(Exception) as e:
			self.log.exception('[[EXCEPTON OCCURED]]: %s', e)
			sys.exit("[[EXCEPTON OCCURED]]please check logfile.")
			
		document-banner-metric ng-scope
		ui-sref="document.full({tab:'citations', q:null, ctx:null, section:null, part:null, anchor:null, tabFilter: 'papers'})"
		#self.save_current_page(driver, "./samples/sample_page2.html")
		self.save_current_page(driver, "./samples/sample_page2.png")
	<button class="load-more-button" type="button" ng-click="vm.loadMoreCitations('patent')" ng-disabled="vm.loading" tabindex="0" aria-disabled="false">
				<span ng-show="!vm.loading" aria-hidden="false" class="">View More</span>
				<i class="fa fa-spinner fa-spin ng-hide" ng-show="vm.loading" aria-hidden="true"></i>
		"""

		cited_papers = []
		cited_urls = []
		driver.get(self.convert_paper_url_to_cited_url(url))
		self.log.debug("WebDriverWait")
		timeout = 10
		try:
			element_present = EC.presence_of_element_located(driver.find_element_by_xpath('//b[@class="ng-binding"]'))
			WebDriverWait(driver, timeout).until(element_present)
		except TimeoutException:
			print("Timed out waiting for page to load")
		except NoSuchElementException:
			self.log.debug("catch NoSuchElementException. EC.presence_of_element_located")
		
		self.save_current_page(driver, "./samples/sample_page1055638_cited.html")
		self.save_current_page(driver, "./samples/sample_page1055638_cited.png")

		##if not cited, load-more-button does not exist.
		##but if cited, load-more-button always exists nevertheless no more paper,
		##and the buttons are hidden.
		try:
			load_more_button = driver.find_element_by_xpath('//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]')
		except NoSuchElementException:
			self.log.debug("catch NoSuchElementException. load_more_button = None")
			load_more_button = None

		if load_more_button:
			load_more_button.click()
			self.log.debug("wait 10 sec")
			import time
			time.sleep(10)
		#from selenium.webdriver.support.ui import WebDriverWait
		#WebDriverWait(driver, 100)
		#driver.find_element_by_class_name('load-more-button').click()
		"""
				<div class="load-more-container ng-hide" ng-show="vm.contextData.paperCitations.ieee.length &lt; +vm.contextData.ieeeCitationCount" aria-hidden="true" style="">
			<button class="load-more-button" type="button" ng-click="vm.loadMoreCitations('ieee')" ng-disabled="vm.loading" tabindex="0" aria-disabled="false">
				<span ng-show="!vm.loading" aria-hidden="false" class="" style="">View More</span>
				<i class="fa fa-spinner fa-spin ng-hide" ng-show="vm.loading" aria-hidden="true" style=""></i>
			</button>
		</div>
		"""
		self.save_current_page(driver, "./samples/sample_page1055638_cited_view_more.html")
		self.save_current_page(driver, "./samples/sample_page1055638_cited_view_more.png")
		

		#paper.insert()
		#print(paper.get_vars())
		
		import table_citations
		
		for citing_paper in citing_papers:
			citations = table_citations.Table_citations(start=paper.id, end=citing_paper.id)
			#citations.insert()
		
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return paper, citing_urls, cited_urls
	

	
	def download_papers_by_keywords(self, driver, path, download_num=25):
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
		
	"""	
	def get_papers_with_breadth_first_search(self, root_url_of_paper):
		
		import math
		math.breadth_first_search(root_url_of_paper, get_citing_papers() )

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("root_url_of_paper["+root_url_of_paper+"]")
		
		citing_urls, cited_urls = ***
		
		for url in citing_urls:
			self.get_papers_with_breadth_first_search(url)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	
	def convert_to_datetime(self, str):
		self.log.warning("!!!incomplete method[" + __class__.__name__ + "." + sys._getframe().f_code.co_name + "]!!!")
		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		return timestamp
	
	def convert_paper_url_to_cited_url(self, url):
		#from
		#http://ieeexplore.ieee.org/document/4116687/
		#to
		#http://ieeexplore.ieee.org/document/4116687/citations?anchor=anchor-paper-citations-ieee&ctx=citations
		return url + "citations?anchor=anchor-paper-citations-ieee&ctx=citations"
	
	
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
	
	
	
	