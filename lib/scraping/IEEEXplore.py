
# -*- coding: utf-8 -*-
import sys, os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException

from http.client import RemoteDisconnected


class IEEEXplore:
	def __init__(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from conf import Conf
		self.conf = Conf()
		from log import Log as l
		self.log = l.getLogger()
		
		self.opt = Search_options()
		self.log.debug("class " + __class__.__name__ + " created.")

	
	def get_papers_of_new_conferences(self, conference_num):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + "(conference_num=" + str(conference_num) + ") start.")
		
		
	def get_papers_by_keywords(self, keywords, num_of_papers="all", search_options="default", path="../../data/tmp/", filename="title", timeout=30):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info("keywords[" + keywords + "], num_of_papers[" + str(num_of_papers) +"]")
		
		driver = self.create_driver(timeout=timeout)
		if search_options == "default":
			search_options = Search_options()

		self.search_by_keywords(driver, keywords, search_options=search_options, timeout=timeout)

		if num_of_papers == "all":
			element = driver.find_element_by_css_selector('div[class="pure-u-1-1 Dashboard-header ng-scope"] > span')
			num_of_papers = int(element.text.split(" ")[-1].replace(",",""))
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")
		
		urls = self.get_urls_of_papers_in_keywords_page(driver, search_options.PerPage, num_of_papers, timeout)
		print("urls.size[" + str(len(urls)) + "]")
		all_papers = []
		all_citing_urls = []
		all_cited_urls = []

		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		from searchs import Searchs
		search = Searchs(limit=num_of_papers)

		for url in urls:
			search.node = url
			paper, citing_urls, cited_urls = self.get_attributes_and_download_pdf(search, driver, path=path, filename=filename)
			print("paper.title[" + paper.title + "]")
			all_papers.append(paper)
			all_citing_urls.extend(citing_urls)
			all_cited_urls.extend(cited_urls)
			self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

		return all_papers, urls, all_citing_urls, all_cited_urls

	def get_papers_of_target_conference(self, conference_name):
		pass
	

	def create_driver(self, top_page="", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("url[" + top_page + "]")
		
		phantomjs_path = self.conf.getconf("phantomJS_pass")
		if top_page == "":
			top_page = self.conf.getconf("IEEE_top_page")
		from selenium import webdriver
		driver = webdriver.PhantomJS(phantomjs_path, service_args=["--webdriver-loglevel=ERROR"])
		self.log.debug("driver.get(" + top_page + ")")
		driver.get(top_page)
		if top_page == self.conf.getconf("IEEE_top_page"):
			self.log.debug("Wait start.")
			try:
				WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//li[@class="Media-articles-item"]'))
			except TimeoutException:
				m = "caught TimeoutException at load the iEEE top page."
				print(m)
				self.log.warning(m)
			except NoSuchElementException:
				m = "caught NoSuchElementException at load the iEEE top page."
				print(m)
				self.log.warning(m)

			self.log.debug("Wait Finished.")

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return driver")
		return driver


	def wait_search_results(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		self.log.debug("Wait start.")
		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//input[@type="checkbox" and @class="search-results-group"]'))
		except TimeoutException:
			m = "caught TimeoutException at load the keywords results page."
			print(m)
			self.log.warning(m)
		except NoSuchElementException:
			m = "caught NoSuchElementException at load the keywords results page."
			print(m)
			self.log.warning(m)

		self.log.debug("Wait Finished.")

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def search_by_keywords(self, driver, keywords, search_options="default", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		
		try:
			driver.find_element_by_name('queryText').send_keys(keywords)
			driver.find_element_by_class_name('Search-submit').click()
		except(Exception) as e:
			self.log.exception('[[EXCEPTON OCCURED]]: %s', e)
			sys.exit("[[EXCEPTON OCCURED]]please check logfile.")
		self.wait_search_results(driver, timeout)

		self.set_options(driver, search_options, timeout)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return 0

	def set_options(self, driver, search_options, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		try:
			#self.save_current_page(driver, "./samples/before_set_options.png")
			#self.save_current_page(driver, "./samples/before_set_options.html")
			##show" : "All Resul

			##PerPage" : "25"
			if search_options.PerPage != 25:
				element = driver.find_element_by_css_selector('div[ng-model="vm.rowsPerPage"] > div > select')
				
				#print(len(element))
				#print(element.text)
				Select(element).select_by_visible_text(str(search_options.PerPage))
				self.wait_search_results(driver, timeout)
			#Select(element).select_by_value("object:75")
			##SortBy" : "MostCit
			##ContentType" : "No
			##YearType" : "Range
			##YearFrom" : "1996"
			##YearTo" : "2017",
			##Year" : "2017",
			##Author" : "None",
			##Affiliation" : "No
			##PublicationTitle" 
			##Publisher" : "None
			##ConferenceLocation
		except NoSuchElementException:
			m = "caught NoSuchElementException at get_citing_papers."
			self.log.warning(m)
			print(m)
			self.save_current_page(driver, "./samples/aNoSuchElementException_in_set_options.png")
			self.save_current_page(driver, "./samples/NoSuchElementException_in_set_options.html")

		
		
		#self.save_current_page(driver, "./samples/after_set_options.png")
		#self.save_current_page(driver, "./samples/after_set_options.html")
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		
		
	
	def get_urls_of_papers_in_keywords_page(self, driver, PerPage, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		
		if num_of_papers == "all":
			#<span ng-if="vm.totalRecords &gt; 1" class="ng-binding ng-scope">Displaying results 1-25 of 39</span>
			#element = driver.find_element_by_xpath('//span[@ng-if="vm.totalRecords &gt; 1" and @class="ng-binding ng-scope"]')
			#element = driver.find_element_by_xpath('//span[@ng-if="vm.totalRecords &gt\; 1"]')
			element = driver.find_element_by_css_selector('div[class="pure-u-1-1 Dashboard-header ng-scope"] > span')
			num_of_papers = int(element.text.split(" ")[-1].replace(",",""))
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")
		
		urls = []
		#self.save_current_page(driver, "./samples/before_click_next.png")
		#self.save_current_page(driver, "./samples/before_click_next.html")

		#button = driver.find_elements_by_xpath('//a[@href="" and @ng-click="selectPage(page.number)" and @class="ng-binding" and @tabindex="0"]')
		#for button in buttons:
		next_button = driver.find_element_by_xpath('//nav[@class="c-Pagination ng-isolate-scope ng-valid"]/ul/li/a[@href="" and @ng-click="selectPage(page.number)" and @class="ng-binding" and @tabindex="0"]')
		visited_buttons = [next_button.text]
		while True:
			self.log.debug("get paper urls in current page")
			for i in range(PerPage):
				paper_elements = driver.find_elements_by_xpath('//div[@class="js-displayer-content u-mt-1 stats-SearchResults_DocResult_ViewMore ng-scope hide"]')
				self.log.debug("len(paper_elements)[" + str(len(paper_elements)) + "]")
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				if len(paper_elements) == PerPage:
					break
			self.log.debug("len(paper_elements)[" + str(len(paper_elements)) + "]")

			for paper_element in paper_elements:
				url = paper_element.find_element_by_css_selector('a').get_attribute("href")
				self.log.debug("url[" + url + "]")
				urls.append(url)
				if len(urls) > num_of_papers:
					self.log.debug("len(urls)[" + str(len(urls)) + "] > num_of_papers[" + str(num_of_papers) + "]. return urls.")
					return urls

			self.log.debug("search button to next page")
			buttons = driver.find_elements_by_xpath('//a[@href="" and @ng-click="selectPage(page.number)" and @class="ng-binding" and @tabindex="0"]')
			i = 0
			for button in buttons:
				self.log.debug("i[" + str(i) + "], button.text[" + button.text + "], visited_buttons:" + str(visited_buttons))
				if not button.text in visited_buttons:
					next_button = button
					self.log.debug("break")
					break
				i+=1
			if i == len(buttons):
				self.log.debug("i = len(buttons). already visited all buttons. break")
				break

			#self.save_current_page(driver, "./samples/after_click_"  + str(next_button.text) + "_footer_of_keyword.png")
			#self.save_current_page(driver, "./samples/after_click_"  + str(next_button.text) + "_footer_of_keyword.html")
			visited_buttons.append(next_button.text)
			self.log.debug("move to next page[" + next_button.text + "]")
			next_button.click()
			self.wait_search_results(driver, timeout)
						
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return urls[" + str(len(urls)) + "]")
		return urls
	
	
	def get_attributes_and_download_pdf(self, search, driver, path="../../data/tmp/", filename="title"):
		print(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#driver = self.create_driver()
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
		timeout = 30
		target_paper_url = search.node
		search.times += 1
		print("url[" + target_paper_url + "], times[" + str(search.times) + "], limit[" + str(search.limit) + "]")
		self.log.info("url[" + target_paper_url + "], times[" + str(search.times) + "], limit[" + str(search.limit) + "]")
		
		##reconnect because of http.client.RemoteDisconnected
		#if search.times % 5 == 0:
		#	driver = self.reconnect_driver(driver, driver.current_url)
		#self.save_current_page(driver, "./samples/tmp.png")

		##if this paper already downloaded, this paper visited and skip.
		#if target_paper_url in search.visited:
		
		self.move_to_paper_initial_page(driver, target_paper_url)

		import table_papers
		paper = table_papers.Table_papers()

		self.log.debug("get attributes of this paper")
		paper.title = self.get_title(driver)
		paper.authors = self.get_authors(driver)
		paper.keywords = self.get_keywords(driver)
		paper.citings, citing_papers, citing_urls = self.get_citing_papers(driver, timeout)
		paper.citeds, cited_papers, cited_urls = self.get_cited_papers(driver, timeout)
		paper.conference = self.get_conference(driver)
		paper.published = self.get_date_of_publication(driver)
		paper.url = target_paper_url
		paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		if filename == "title":
			filename = paper.title + ".pdf"
		paper.path = self.download_a_paper(driver, path=path, filename=filename, timeout=timeout)
		self.log.debug("download finished. wait start.")
		time.sleep(self.conf.getconf("IEEE_wait_time_per_download_paper"))
		self.log.debug("wait finished.")
		paper.id = paper.get_id()
		
		self.log.debug(paper.get_vars())
		paper.renewal_insert()
		
		self.log.debug("insert citations of this paper to db")
		import table_citations
		
		for citing_paper in citing_papers:
			citation = table_citations.Table_citations(start=paper.id, end=citing_paper.id)
			citation.renewal_insert()
			citation.close()
		for cited_paper in cited_papers:
			citation = table_citations.Table_citations(start=cited_paper, end=paper.id)
			citation.renewal_insert()
			citation.close()
		
		self.log.debug("check termination of searching loop")
		if 0 < search.limit and search.times >= search.limit:
			self.log.debug("search finished.")
			search.que = [search.node]
			import signal
			driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
			driver.quit() # quit the node proc
			return paper, [], []
			
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return paper[" + paper.title + "] citing_urls[" + str(citing_urls) + "] cited_urls[" + str(cited_urls) + "]")
		return paper, citing_urls, cited_urls
	
	
	
	def get_title(self, driver):
		#element = driver.find_element_by_tag_name("title")
		#element = driver.find_element_by_id("title")
		#element = driver.find_element_by_css_selector("html > title")
		#element = driver.find_element_by_class_name("title")
		return driver.title
		
	
	def get_authors(self, driver):
		##authors
		#<span ng-bind-html="::author.name" class="ng-binding">
		#elements = driver.find_elements_by_class_name("authors-container")
		#print(str(len(elements)))
		authors_str = ""
		elements = driver.find_elements_by_xpath('//span[@ng-bind-html="::author.name"]')
		#print(str(len(elements))) #5
		for el in elements:
			authors_str += ","+el.text
		return authors_str[1:]
	
	def get_keywords(self, driver):
		##keywords
		keywords_str = ""
		elements = driver.find_elements_by_xpath('//a[@ng-bind-html="::term"]')
		#print(str(len(elements))) #21
		for el in elements:
			keyword = el.text
			if keyword in keywords_str:
				##todo internet concludes int
				self.log.debug("keyword[" + keyword + "] is deplicated. not add.")
			else:
				keywords_str += ","+el.text
		return keywords_str
	
	def get_citing_papers(self, driver, timeout=30):
		##citing_papers
		##citing_urls
		"""
					<a ng-href="/document/4116687" title="Usilng Machine Learning Technliques to Identify Botnet Traffic" target="_self" href="/document/4116687">
				<span ng-bind-html="::(vm.contextData.isStandard ? article.standardNumber + ' - ' + article.title : article.title) | charlimitHtml:185" mathjax-bind="" class="ng-binding">Usilng Machine Learning Technliques to Identify Botnet Traffic</span>
			</a>
			<div class="ng-binding">Carl Livadas; Robert Walsh; David Lapsley; W. Timothy Strayer</div>
		</div><!-- end ngRepeat: article in vm.contextData.similar --><div class="doc-all-related-articles-list-item ng-scope" ng-repeat="article in vm.contextData.similar"> 
		"""
		import table_papers
		citings_str = ""
		citing_papers = []
		citing_urls = []
		
		try:
			elements = driver.find_elements_by_css_selector('div[ng-repeat="article in vm.contextData.similar"]')
		except NoSuchElementException:
			m = "caught NoSuchElementException at get_citing_papers."
			self.log.warning(m)
			print(m)
		
		self.log.debug(str(len(elements)))
		#self.save_current_page(driver, "./samples/sample_page_4116687_start.html")
		#self.save_current_page(driver, "./samples/sample_page_4116687_start.png")
		self.log.debug("create arrays of paper and url")

		for el in elements:
			citing_paper = table_papers.Table_papers()
			citing_paper.url = self.conf.getconf("IEEE_website") + el.find_element_by_css_selector('a').get_attribute("ng-href")
			citing_paper.title = el.find_element_by_css_selector('a').get_attribute("title")
			citing_paper.authors = el.find_element_by_css_selector('div[class="ng-binding"]').text.replace(";", ",")
			import time
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			self.log.debug("citing_url[" + citing_paper.url + "]")
			self.log.debug("citing_title[" + citing_paper.title + "]")
			self.log.debug("citing_authors[" + citing_paper.authors + "]")
			self.log.debug(citing_paper.get_vars())

			citing_paper.renewal_insert()
			citing_papers.append(citing_paper)
			citing_urls.append(citing_paper.url)
			
		return citings_str, citing_papers, citing_urls
	
	
	def get_cited_papers(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		import table_papers
		
		citeds_str = ""
		cited_papers = []
		cited_urls = []

		#href="/document/4116687/citations?tabFilter=papers"
		#http://ieeexplore.ieee.org/document/4116687/citations?anchor=anchor-paper-citations-ieee&ctx=citations
		initial_url = driver.current_url
		driver.get(self.convert_paper_url_to_cited_url(initial_url))
		#self.save_current_page(driver, "./samples/sample_page_1055638_start.html")
		#self.save_current_page(driver, "./samples/sample_page_1055638_start.png")
		
		"""
		<div ng-if="!vm.loading &amp;&amp; !vm.details.paperCitations.ieee &amp;&amp; !vm.details.paperCitations.nonIeee &amp;&amp; !vm.details.patentCitations" class="ng-scope" style="">
		Citations are not available for this document.
	</div>
		"""
		#el = driver.find_element_by_xpath('//div[@ng-if="!vm.loading &amp;&amp; !vm.details.paperCitations.ieee &amp;&amp; !vm.details.paperCitations.nonIeee &amp;&amp; !vm.details.patentCitations"')
		#els = driver.find_elements_by_xpath('//div[@class="ng-scope" and @style=""]') #ok. got els
		#els = driver.find_elements_by_xpath('//div[@ng-if="::!vm.contextData.paperCitations.ieee &amp;&amp; !vm.contextData.paperCitations.nonIeee &amp;&amp; !vm.contextData.patentCitations"]') #0
                                             #><div ng-if="::!vm.contextData.paperCitations.ieee &amp;&amp; !vm.contextData.paperCitations.nonIeee &amp;&amp; !vm.contextData.patentCitations" class="ng-scope">
		#els = driver.find_elements_by_xpath('//div[@ng-if="::!vm.contextData.paperCitations.ieee"]') #0
		try:
			div = driver.find_element_by_css_selector('div > section[class="document-all-references ng-scope"] > div[class="ng-scope"] > div[class="strong"]').text
			if div == "Citations not available for this document.":
				self.log.debug("this paper not cited. return []")
				return citeds_str, cited_papers, cited_urls
			self.log.debug("div="+div+", this paper is cited")
		except NoSuchElementException:
			self.log.debug("this paper is cited")

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
		self.log.debug("WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//b[@class=ng-binding]' start")

		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//b[@class="ng-binding"]'))
		except TimeoutException:
			m = "caught TimeoutException at load the first cited page."
			print(m)
			self.log.warning(m)
			self.move_to_paper_initial_page(driver, initial_url)
			return citeds_str, cited_papers, cited_urls
		except NoSuchElementException:
			m = "caught NoSuchElementException at load the first cited page."
			print(m)
			self.log.warning(m)
			self.move_to_paper_initial_page(driver, initial_url)
			return citeds_str, cited_papers, cited_urls
			
		self.log.debug("Wait Finished.")
		
		#self.save_current_page(driver, "./samples/sample_page_1055638_cited.html")
		#self.save_current_page(driver, "./samples/sample_page_1055638_cited.png")

		self.log.debug("continue pushing more view button")
		elements = self.continuous_pushing_more_view_button(driver, timeout)
		
		self.log.debug("create arrays of paper and url")
		
		for el in elements:
			cited_url = self.conf.getconf("IEEE_website") + el.find_element_by_css_selector('div[class="ref-links-container stats-citations-links-container"] > span > a').get_attribute("ng-href")
			cited_urls.append(cited_url)
			cited_authors, cited_title, cited_conference, cited_date = self.parse_citing(el.find_element_by_css_selector('div[ng-bind-html="::item.displayText"]').text)
			import time
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			cited_paper = table_papers.Table_papers(title=cited_title, authors=cited_authors, conference=cited_conference, published=cited_date, url=cited_url, timestamp=timestamp)
			self.log.debug(cited_paper.get_vars())
			cited_paper.renewal_insert()
			
		#self.save_current_page(driver, "./samples/sample_page_cited_view_more.html")
		#self.save_current_page(driver, "./samples/sample_page_cited_view_more.png")
			
		self.move_to_paper_initial_page(driver, initial_url)
		#self.save_current_page(driver, "./samples/sample_page_initial.html")
		#self.save_current_page(driver, "./samples/sample_page_initial.png")


		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return citeds_str, cited_papers, cited_urls
		
	
	def continuous_pushing_more_view_button(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##if not cited, load-more-button does not exist.
		##but if cited, load-more-button always exists nevertheless no more paper,
		##and the buttons are hidden.
		
		elements = driver.find_elements_by_css_selector('div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]')
		num_of_viewing = len(elements)
		limit_of_view = self.conf.getconf("IEEE_citation_num_at_first_page")
		self.log.debug("num_of_viewing[" + str(num_of_viewing) + "], limit_of_view[" + str(limit_of_view) + "]")
		
		while num_of_viewing > limit_of_view - 10:
			limit_of_view += self.conf.getconf("IEEE_citation_num_per_more_view")
			try:
				load_more_button = driver.find_element_by_xpath('//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]')
				load_more_button.click()

				WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')" and @aria-disabled="false"]'))
			except TimeoutException:
				m = "caught TimeoutException at loading more cited pages(" + str(limit_of_view) + ") paper[" + driver.current_url + "]."
				print(m)
				self.log.warning(m)
			except NoSuchElementException:
				m = "caught NoSuchElementException at loading more cited pages(" + str(limit_of_view) + ") paper[" + driver.current_url + "]."
				print(m)
				self.log.warning(m)
			except ElementNotVisibleException:
				m = "caught ElementNotVisibleException at loading more cited pages(" + str(limit_of_view) + ") paper[" + driver.current_url + "]. break."
				self.log.debug(m)
				break
				
			elements = driver.find_elements_by_css_selector('div[ng-repeat="item in vm.contextData.paperCitation"]')
			num_of_viewing = len(elements)
			self.log.debug("num_of_viewing[" + str(num_of_viewing) + "], limit_of_view[" + str(limit_of_view) + "]")
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return elements
	
	
	def get_conference(self, driver):
		try:
			return driver.find_element_by_xpath('//div[@class="u-pb-1 stats-document-abstract-doi ng-scope"]')\
							.find_element_by_tag_name('a').text
		except NoSuchElementException:
			return ""

		
	
	def get_date_of_publication(self, driver):
			#Date of Publication: 06 January 200 or Date of Conference 14-16 Nov. 2006
		try:
			date = driver.find_element_by_xpath('//div[@ng-if="::vm.details.isConference == true"]').text
		except NoSuchElementException:
			self.log.debug("catch NoSuchElementException. date = ''") ##todo paper
			date = ""
		return self.convert_to_datetime(date)
	
	
	def move_to_paper_initial_page(self, driver, initial_url, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		driver.get(initial_url)
		self.log.debug("WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//div[@ng-repeat=\"article in vm.contextData.similar\"]'))")

		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//div[@ng-repeat="article in vm.contextData.similar"]'))
		except TimeoutException:
			m = "caught TimeoutException at load the paper top page."
			print(m)
			self.log.warning(m)
		except NoSuchElementException:
			m = "caught NoSuchElementException at load the paper top page."
			print(m)
			self.log.warning(m)
			
		self.log.debug("Wait Finished.")

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	def wait_button_to_pdf_page(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("Wait start.")
		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_css_selector('i[class="icon doc-act-icon-pdf"]'))
		except TimeoutException:
			m = "caught TimeoutException at waiting button which go to pdf page."
			print(m)
			self.log.warning(m)
		except NoSuchElementException:
			m = "caught NoSuchElementException at waiting button which go to pdf page."
			print(m)
			self.log.warning(m)
		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		
	
	
	def download_a_paper(self, driver, path="../../data/tmp/", filename="default", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url
		
		m = "downloading paper to " + path + ". title[" + filename + "]"
		self.log.info(m)
		print(m)

		self.wait_button_to_pdf_page(driver, timeout)
		
		#button = driver.find_element_by_css_selector('li[class="large doc-actions-item"]')
		button = driver.find_element_by_css_selector('i[class="icon doc-act-icon-pdf"]')
		#self.save_current_page(driver, "./samples/get_button.html")
		#self.save_current_page(driver, "./samples/get_button.png")
		
		retries = 10
		while retries > 0:
			try:
				button.click()
				self.log.debug("clicked button and no exception. break")
				break
			except RemoteDisconnected:
				m = "caught RemoteDisconnected at click download pdf button. retries[" + str(retries) + "]"
				print(m)
				self.log.warning(m)
				import time
				time.sleep(self.conf.getconf("IEEE_wait_time_per_download_paper"))
				retries -= 1
			except ConnectionRefusedError:
				m = "caught ConnectionRefusedError at click download pdf button. retries[" + str(retries) + "]"
				print(m)
				self.log.warning(m)
				import time
				time.sleep(self.conf.getconf("IEEE_wait_time_per_download_paper"))
				driver.get(initial_url)
				self.wait_button_to_pdf_page(driver, timeout)
				button = driver.find_element_by_css_selector('i[class="icon doc-act-icon-pdf"]')
				retries -= 1
			except NoSuchElementException:
				m = "caught NoSuchElementException at click download pdf button. retries[" + str(retries) + "]"
				print(m)
				self.log.warning(m)
				self.save_current_page(driver, "./samples/caught_NoSuchElementException_at_click_download_pdf_button.html")
				self.save_current_page(driver, "./samples/caught_NoSuchElementException_at_click_download_pdf_button.png")
				retries -= 1
		if retries == 0:
			self.log.error("button.click() error")
			self.save_current_page(driver, "./samples/button_click_error.html")
			self.save_current_page(driver, "./samples/button_click_error.png")

		self.log.debug("Wait start.")
		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath('//frameset[@rows="65,35%"]/frame'))
		except TimeoutException:
			m = "caught TimeoutException at load the iEEE pdf page."
			print(m)
			self.log.warning(m)
		except NoSuchElementException:
			m = "caught NoSuchElementException at load the iEEE pdf page."
			print(m)
			self.log.warning(m)
		self.log.debug("Wait Finished.")
		url = driver.find_elements_by_xpath('//frameset[@rows="65,35%"]/frame')[1].get_attribute("src")
		self.log.debug("url:" + url)
		
		if filename == "default":
			filename = url[:url.index("?")].split("/")[-1]
		filename = filename.replace(":", "")
		self.log.debug("filename:" + filename)
		command = "wget -p \"" + url + "\" -O \"" + path + filename + "\" > /dev/null 2>&1"
		#command = "wget -p \"" + url + "\" -O \"" + path + filename + "\" 1> /dev/null 2>&1"
		#command = "wget -p \"" + url + "\" -O \"" + path + filename + "\""
		self.log.debug(command)
		try:
			self.log.debug(os.system(command))
		except:
			m = "error at " + command
			self.log.warning(m)
			print(m)
			

		#self.save_current_page(driver, "./samples/7898372.png")
		#self.save_current_page(driver, "./samples/7898372.html")

		driver.get(initial_url)
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return[" + path + filename + "]")
		return path + filename
		
		
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
			
			self.log.debug("pdf_title:"+pdf_title)
			self.log.debug("pdf_dir:"+pdf_url)
			self.log.debug("pdf_author:" + str(pdf_authors))
			
			i+=1
			if i >= download_num:
				self.log.debug("i>="+str(download_num)+"."+__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
				return 0
		self.log.debug("len(link)<"+str(download_num)+"."+__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
		return 0
	
	def convert_to_datetime(self, str):
		self.log.warning("!!!incomplete method[" + __class__.__name__ + "." + sys._getframe().f_code.co_name + "]!!!")
		import time
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		return timestamp
	
	
	def convert_paper_url_to_cited_url(self, url):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#from
		#http://ieeexplore.ieee.org/document/4116687/?reload=true
		#to
		#http://ieeexplore.ieee.org/document/4116687/citations?anchor=anchor-paper-citations-ieee&ctx=citations
		self.log.debug("url[" + url + "]")
		converted_url = url.split("?")[0] + "citations?anchor=anchor-paper-citations-ieee&ctx=citations"
		self.log.debug("converted_url[" + converted_url + "]")
		
		return converted_url
		
	
	def convert_paper_url_to_pdf_url(self, url):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##from
		##http://ieeexplore.ieee.org/document/6324382/
		##to
		##http://ieeexplore.ieee.org/ielx7/35/7901458/07901477.pdf?tp=&arnumber=7901477&isnumber=7901458
		print("url[" + url + "]")
	
	
	
	def parse_citing(self, strings):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("src_srt["+strings+"]")
		#from
		#Daniel Garant, Wei Lu, "Mining Botnet Behaviors on the Large-Scale Web Application Community", Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on, pp. 185-190, 2013.
		#to
		#Daniel Garant, Wei Lu, 
		#Mining Botnet Behaviors on the Large-Scale Web Application Community
		#Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on
		#pp. 185-190, 2013
		array = strings.split("\"")
		if len(array) < 3:
			self.log.warning(__class__.__name__ + "." + sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(array)(" + str(len(array)) + ") < 3. return \"\", \"\", \"\", \"\"")
			return "", "", "", ""

		authors = array[0]
		title = array[1]
		new_array = array[2][1:].split(",")
		self.log.debug("new_array:" + str(new_array))
		self.log.debug(len(new_array))
		if len(new_array) < 3:
			self.log.warning(__class__.__name__ + "." + sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(new_array)(" + str(len(new_array)) + ") < 3. return authors, title, \"\", \"\"")
			return authors, title, "", ""

		elif len(new_array) == 3:
			conference, page, year = new_array
		elif len(new_array) == 4:
			conference, vol, page, year = new_array
		elif len(new_array) == 5:
			conference, vol, page, year, issn = new_array
		else:
			self.log.warning(__class__.__name__ + "." + sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(new_array)(" + str(len(new_array)) + ") > 5. return authors, title, \"\", \"\"")
			return authors, title, "", ""
		import re
		#self.log.debug("re.match(\"\d*\", " + year + ")")
		#year = re.match("*\d*",year).group() + "-01-01 00:00:00"
		#year += "-01-01 00:00:00"
		self.log.debug("citing year is none")
		year = None
		self.log.debug("authors[" + str(authors) + "], title[" + str(title) + "], conference[" + str(conference) + "], year[" + str(year) + "]")
		return authors, title, conference, year
		
		
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

	def reconnect_driver(self, driver, url):
			self.log.debug("driver reconnect")
			import signal
			driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
			driver.quit() # quit the node proc
			driver = self.create_driver(url)
			return driver

class Search_options:

	show = "All Results"
	PerPage = 25
	SortBy = "MostCited[ByPapers]"
	ContentType = "None"
	YearType = "Range"
	YearFrom = 1996
	YearTo = 2017
	Year = 2017
	Author = None
	Affiliation = None
	PublicationTitle = None
	Publisher = None
	ConferenceLocation = None

	def __init__(self):
		import sys,os
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()
		
		self.log.debug("class " + __class__.__name__ + " created.")
	
	def show_options(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		import inspect
		methods = []
		for method in inspect.getmembers(self, inspect.ismethod):
			methods.append(method[0])

		for var in self.__dir__():
			if not var.startswith("_") and var != "log" and not var in methods:
				print(var + "[" + str(eval("self."+var)) + "]")
		#for key, value in self.opts.items():
		#	print(key + "[" +value +"]")
	def a(self):
		pass

