
# -*- coding: utf-8 -*-

import sys, os
import time
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException

from http.client import RemoteDisconnected
from urllib.request import URLError

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
from table_papers import Table_papers
from table_citations import Table_citations
from table_authors import Table_authors



class IEEEXplore:
	def __init__(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
		from conf import Conf
		self.conf = Conf()
		from log import Log as l
		self.log = l.getLogger()

		self.opts = Search_options()
		self.log.debug("class " + __class__.__name__ + " created.")


	def get_attributes_and_download_pdf(self, search, driver, path="../../data/tmp/", filename="title", timeout=30):
		print(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		search.times += 1
		target_paper_url = search.node

		m = "url[" + target_paper_url + "]\ntimes[" + str(search.times) + "], len(que)[" + str(len(search.que)) + "], limit[" + str(search.limit) + "]"
		print(m)
		self.log.info(m)

		self.move_to_paper_initial_page(driver, target_paper_url)

		paper = Table_papers(title=self.get_title(driver))
		##if this paper already downloaded recently, this paper had visited and skip.
		if paper.has_already_downloaded():
			self.log.debug("paper.has_already_downloaded. return paper, paper.url, [], [], " + str(paper.get_citings_array()) + ", " + str(paper.get_citeds_array()) + ", []")
			return [paper, paper.url, [], [], paper.get_citings_array(), paper.get_citeds_array(), []]


		self.log.debug("get attributes of this paper")
		self.log.debug("get authors")
		if search.times + len(search.que) <= search.limit:
			paper.authors, urls_of_papers_with_same_authors = self.get_authors_and_urls_of_papers_with_same_authors(driver, num_of_papers=self.conf.getconf("IEEE_num_of_spreading_by_author"), timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.authors = self.get_authors(driver)
			urls_of_papers_with_same_authors = []

		self.log.debug("get keywords")
		if search.times + len(search.que) <= search.limit:
			paper.keywords, urls_of_papers_with_same_keywords = self.get_keywords_and_urls_of_papers_with_same_keywords(driver, num_of_papers=self.conf.getconf("IEEE_num_of_spreading_by_keyword"), timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.keywords = self.get_keywords(driver)
			urls_of_papers_with_same_keywords = []

		self.log.debug("get citing papers")
		paper.citings, citing_papers, citing_urls = self.get_citing_papers(driver, timeout)

		self.log.debug("get cited papers")
		paper.citeds, cited_papers, cited_urls = self.get_cited_papers(driver, timeout)

		self.log.debug("get conference")
		if search.times + len(search.que) <= search.limit:
			paper.conference, urls_in_conference = self.get_conference_and_urls_of_papers_in_same_conference(driver, num_of_papers=self.conf.getconf("IEEE_num_of_spreading_by_conference"), timeout=timeout)
		else:
			paper.conference = get_conference(driver)
			urls_in_conference = []
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

		for citing_paper in citing_papers:
			citing_paper.renewal_insert()
			citation = Table_citations(start=paper.id, end=citing_paper.id)
			citation.renewal_insert()
			citing_paper.close()
			citation.close()
		for cited_paper in cited_papers:
			cited_paper.renewal_insert()
			citation = Table_citations(start=cited_paper.id, end=paper.id)
			citation.renewal_insert()
			cited_paper.close()
			citation.close()

		self.log.debug("check termination of searching loop")
		if 0 < search.limit and search.times >= search.limit:
			self.log.debug("search finished. 0 < search.limit and search.times >= search.limit.")
			self.log.debug("return [paper, paper.url, [], [], [], [], []]")
			search.que = [search.node]
			return [paper, paper.url, [], [], [], [], []]
		elif search.times + len(search.que) > search.limit:
			self.log.debug("search.times + len(search.que) < search.limit")
			self.log.debug("return [paper, paper.url, [], [], [], [], []]")
			search.que = [search.node]
			return [paper, paper.url, [], [], [], [], []]
		else:
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
			self.log.debug("return [paper[" + paper.title + "], paper_url[" + paper.url + "] citing_urls[" + str(citing_urls) + "] cited_urls[" + str(cited_urls) + "]]")
			return [paper, paper.url, urls_of_papers_with_same_authors, urls_of_papers_with_same_keywords, citing_urls, cited_urls, urls_in_conference]


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

		urls = self.get_urls_of_papers_in_search_results(driver, num_of_papers, timeout)
		print("urls.size[" + str(len(urls)) + "]")

		all_papers = []
		all_urls_of_papers_with_same_authors = []
		all_urls_of_papers_with_same_keywords = []
		all_citing_urls = []
		all_cited_urls = []
		all_urls_in_conference = []

		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		from searchs import Searchs
		search = Searchs(limit=num_of_papers)

		for url in urls:
			search.node = url
			[paper, paper_url, urls_of_papers_with_same_authors, urls_of_papers_with_same_keywords, citing_urls, cited_urls, urls_in_conference] = self.get_attributes_and_download_pdf(search, driver, path=path, filename=filename)
			all_papers.append(paper)
			all_urls_of_papers_with_same_authors.extend(urls_of_papers_with_same_authors)
			all_urls_of_papers_with_same_keywords.extend(urls_of_papers_with_same_keywords)
			all_citing_urls.extend(citing_urls)
			all_cited_urls.extend(cited_urls)
			all_urls_in_conference.extend(urls_in_conference)
			self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

		return all_papers, urls, all_urls_of_papers_with_same_authors, all_urls_of_papers_with_same_keywords, all_citing_urls, all_cited_urls, all_urls_in_conference


	def get_papers_of_target_conference(self, conference_name):
		pass

		
	def get_papers_of_new_conferences(self, conference_num):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + "(conference_num=" + str(conference_num) + ") start.")

		
	def search_by_keywords(self, driver, keywords, search_options="default", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		driver.wait_appearance_of_tag(by="name", tag='queryText', timeout=timeout)
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



	def get_urls_of_papers_in_search_results(self, driver, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		if num_of_papers == "all":
			element = driver.find_element_by_css_selector('div[class="pure-u-1-1 Dashboard-header ng-scope"] > span')
			results = element.text.split(" ")
			self.log.debug("num of search result string[" + str(len(results)) + "]")
			if results[3] == "1":
				num_of_papers = 1
			else:
				#self.log.debug(results[-1])
				#driver.save_current_page("../../var/ss/search_by_author_get_num_ok.png")
				#driver.save_current_page("../../var/ss/search_by_author_get_num_ok.html")
				num_of_papers = int(results[-1].replace(",",""))
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")
		
		self.opts.set_PerPage(num_of_papers)
		self.set_options(driver, self.opts, timeout=timeout)

		urls = []

		next_button = driver.find_element_by_xpath('//a[@href="" and @ng-click="selectPage(page.number)" and @class="ng-binding"]')
		visited_buttons = [next_button.text]
		while True:
			self.log.debug("get paper urls in current page")
			for i in range(self.opts.PerPage):
				paper_elements = driver.find_elements_by_xpath('//div[@class="js-displayer-content u-mt-1 stats-SearchResults_DocResult_ViewMore ng-scope hide"]')
				self.log.debug("scroll times["+str(i)+"] len(paper_elements)[" + str(len(paper_elements)) + "]")
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				if len(paper_elements) == self.opts.PerPage:
					break
			self.log.debug("len(paper_elements)[" + str(len(paper_elements)) + "]")

			for paper_element in paper_elements:
				url = paper_element.find_element_by_css_selector('a').get_attribute("href")
				self.log.debug("url[" + url + "]")
				urls.append(url)
				if len(urls) >= num_of_papers:
					self.log.debug("len(urls)[" + str(len(urls)) + "] > num_of_papers[" + str(num_of_papers) + "]. return urls.")
					return urls

			self.log.debug("search buttons to next page")
			buttons = driver.find_elements_by_xpath('//a[@href="" and @ng-click="selectPage(page.number)" and @class="ng-binding"]')
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

			visited_buttons.append(next_button.text)
			self.log.debug("move to next page[" + next_button.text + "]")
			next_button.click()
			self.wait_search_results(driver, timeout)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return urls[" + str(len(urls)) + "]")
		return urls

	def get_urls_of_papers_in_conference(self, driver, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url

		if num_of_papers == "all":
			elements = driver.find_elements_by_css_selector('div[class="results-display"] > b')
			if len(elements) == 2:
				num_of_papers = int(elements[1].text)
			else:
				self.log.warning("at get_urls_of_papers_in_conference")
				self.log.warning("num_of_papers == all and len(elements) != 2")
				filename = "../../var/ss/get_urls_of_papers_in_conference_len_not_equal_2"
				self.log.warning("save to " + filename)
				driver.save_current_page(filename + ".png")
				driver.save_current_page(filename + ".html")
				num_of_papers=100000000000
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")

		self.opts.set_PerPage(num_of_papers)
		driver.get(driver.current_url + "&rowsPerPage=" + str(self.opts.PerPage))
		if not self.wait_conference_page(driver, timeout):
			self.log.debug("cannot read conference page: " + conference_url)
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return []")
			return []
		#driver.save_current_page("../../var/ss/set_perpage_and_wait.png")
		#driver.save_current_page("../../var/ss/set_perpage_and_wait.html")

		urls = []
		visited_buttons = []
		while True:
			self.log.debug("get paper urls in current page")
			#paper_elements = driver.find_elements_by_xpath('//input[@type="hidden" and @name="submitAbsUrl" and @id="submitAbsUrl" and @value="/xpl/articleDetails.jsp"]/h3/a')
			paper_elements = driver.find_elements_by_xpath('//h3/a')
			self.log.debug("len(paper_elements)[" + str(len(paper_elements)) + "]")
			for el in paper_elements:
				urls.append(el.get_attribute("href"))
				if len(urls) >= num_of_papers:
					self.log.debug("len(urls)[" + str(len(urls)) + "] >= num_of_papers[" + str(num_of_papers) + "]")
					driver.get(initial_url)
					self.wait_conference_page(driver, timeout)
					self.log.debug("get_urls_of_papers_in_conference finished. return urls: " + str(urls))
					return urls

			self.log.debug("search buttons to next page")
			try:
				next_button = driver.find_element_by_xpath('//div[@class="pagination"]/a[@href="#" and @aria-label="Pagination Next Page" and @class="next ir"]')
			except NoSuchElementException as e:
				self.log.warning("caught " + e.__class__.__name__ + " at get_urls_of_papers_in_conference.")
				self.log.warning("Does not this page have next button? please check url[" + driver.current_url + "]")
				self.log.warning("break")
				break

			next_button_attribute = next_button.get_attribute("onclick")
			if next_button_attribute in visited_buttons:
				self.log.debug("visited all button. break")
				break
			visited_buttons.append(next_button_attribute)
			self.log.debug("visited_buttons: " + str(visited_buttons))
			self.log.debug("move to next page[" + next_button_attribute + "]")
			next_button.click()
			if not self.wait_conference_page(driver, timeout):
				self.log.warning("cannot read conference next page: " + driver.current_url)
				self.log.warning("break")
				break

		driver.get(initial_url)
		self.wait_conference_page(driver, timeout)
		self.log.debug("get_urls_of_papers_in_conference finished. return urls: " + str(urls))
		return urls

	def get_title(self, driver):
		return driver.title


	def get_authors(self, driver):
		authors_str = ""
		elements = driver.find_elements_by_xpath('//span[@ng-bind-html="::author.name"]')

		for el in elements:
			authors_str += ","+el.text
		return authors_str[1:]

	def get_authors_and_urls_of_papers_with_same_authors(self, driver, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url

		driver.wait_appearance_of_tag(by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')
		try:
			#elements = driver.find_elements_by_xpath('//span[@ng-bind-html="::author.name"]')
			#elements = driver.find_elements_by_xpath('//a[@qtip-popover="" and @qtip-event-show="hover" and @qtip-event-hide="mouseleave"]')
			elements = driver.find_elements_by_xpath('//span[@class="authors-info ng-binding ng-scope" and @ng-repeat="author in vm.authors"]/span[@ng-if="::author.affiliation" or @ng-if="::!author.affiliation"]/a')
		except NoSuchElementException as e:
			self.log.warning("caught " + e.__class__.__name__ + " at find authors elements.")
			self.log.warning("Does this page have no author? please check url[" + driver.current_url + "]")
		self.log.debug("len(authors_elements)[" + str(len(elements)) + "]")
		#driver.save_current_page("../../var/ss/tmp.png")
		#driver.save_current_page("../../var/ss/tmp.html")

		authors_str = ""
		urls_of_authors = []
		urls_of_papers_with_same_authors = []

		for el in elements:
			author_name = el.find_element_by_xpath('span[@ng-bind-html="::author.name"]').text
			self.log.debug("author_name[" + author_name + "]")
			if "," + author_name in authors_str:
				self.log.debug("author_name[" + author_name + "] is deplicated. not add.")
			else:
				authors_str += ","+author_name
				author = Table_authors()
				author.name = author_name
				urls_of_authors.append(self.conf.getconf("IEEE_website") + el.get_attribute("ng-href"))
				belonging = el.get_attribute("qtip-text")
				author.belonging = belonging
				self.log.debug("author: " + author.get_vars())
				author.renewal_insert()
		authors_str.lstrip(",")

		for link in urls_of_authors:
			driver.get(link)
			self.wait_search_results(driver, timeout)
			urls_of_papers_with_same_authors.extend(self.get_urls_of_papers_in_search_results(driver, num_of_papers, timeout))
		## delete duplicated elements
		urls_of_papers_with_same_authors = list(set(urls_of_papers_with_same_authors))

		self.move_to_paper_initial_page(driver, initial_url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return authors_str, urls_of_papers_with_same_authors
		

	def get_keywords(self, driver):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##keywords
		keywords_str = ""
		elements = driver.find_elements_by_xpath('//a[@ng-bind-html="::term"]')
		for el in elements:
			keyword = el.text
			if "," + keyword in keywords_str:
				self.log.debug("keyword[" + keyword + "] is deplicated. not add.")
			else:
				keywords_str += ","+el.text
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return: " + keywords_str)
		return keywords_str
	
	def get_keywords_and_urls_of_papers_with_same_keywords(self, driver, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url
		driver.wait_appearance_of_tag(by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')
		try:
			elements = driver.find_elements_by_xpath('//a[@ng-bind-html="::term"]')
		except NoSuchElementException as e:
			self.log.warning("caught " + e.__class__.__name__ + " at find keywords elements.")
			self.log.warning("Does this page have no keyword? please check url[" + driver.current_url + "]")
		self.log.debug("len(keywords)[" + str(len(elements)) + "]")

		keywords_str = ""
		urls_of_keywords = []
		urls_of_papers_with_same_keywords = []
		
		for el in elements:
			keyword = el.text
			self.log.debug("keyword[" + keyword + "]")
			if "," + keyword in keywords_str:
				self.log.debug("keyword[" + keyword + "] is deplicated. not add.")
			else:
				keywords_str += ","+keyword
				link = el.get_attribute("href")
				self.log.debug("link[" + link + "]")
				urls_of_keywords.append(link)
		keywords_str.lstrip(",")
		for link in urls_of_keywords:
			driver.get(link)
			self.wait_search_results(driver, timeout)
			urls_of_papers_with_same_keywords.extend(self.get_urls_of_papers_in_search_results(driver, num_of_papers, timeout))
		## delete duplicated elements
		urls_of_papers_with_same_keywords = list(set(urls_of_papers_with_same_keywords))

		self.move_to_paper_initial_page(driver, initial_url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return keywords_str, urls_of_papers_with_same_keywords


	
		
	def get_citing_papers(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		citings_str = ""
		citing_papers = []
		citing_urls = []

		try:
			elements = driver.find_elements_by_css_selector('div[ng-repeat="article in vm.contextData.similar"]')
		except NoSuchElementException:
			self.log.debug("caught NoSuchElementException at get_citing_papers.")
			self.log.debug("this paper has no citing paper. retrun []")
			return citings_str, citing_papers, citing_urls
		self.log.debug("num of citings[" + str(len(elements)) + "]")

		self.log.debug("create arrays of paper and url")
		for el in elements:
			citing_paper =Table_papers()
			citing_paper.url = self.conf.getconf("IEEE_website") + el.find_element_by_css_selector('a').get_attribute("ng-href")
			citing_paper.title = el.find_element_by_css_selector('a').get_attribute("title")
			citing_paper.authors = el.find_element_by_css_selector('div[class="ng-binding"]').text.replace(";", ",")
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			self.log.debug("citing_paper.title: " + citing_paper.title)
			self.log.debug("citing_paper: " + citing_paper.get_vars())

			citings_str += ","+citing_paper.url
			citing_papers.append(citing_paper)
			citing_urls.append(citing_paper.url)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return " + citings_str.lstrip(","))
		return citings_str.lstrip(","), citing_papers, citing_urls


	def get_cited_papers(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		citeds_str = ""
		cited_papers = []
		cited_urls = []

		initial_url = driver.current_url
		driver.get(self.convert_paper_url_to_cited_url(initial_url))

		self.log.debug("wait appearance of cited papers button. wait_appearance_of_tag(by=\"xpath\", tag='//b[@class=\"ng-binding\"]', warning_messages=False) start")
		if not driver.wait_appearance_of_tag(by="xpath", tag='//b[@class="ng-binding"]', warning_messages=False, timeout=timeout):
			self.log.debug("button not appeared. this paper not cited. return []")
			self.move_to_paper_initial_page(driver, initial_url)
			return citeds_str, cited_papers, cited_urls

		self.log.debug("continue pushing more view button")
		elements = self.continuous_pushing_more_view_button(driver, timeout)
		self.log.debug("len(elements): " + str(len(elements)))

		self.log.debug("create arrays of papers and urls")
		for el in elements:
			cited_url = self.conf.getconf("IEEE_website") + el.find_element_by_css_selector('div[class="ref-links-container stats-citations-links-container"] > span > a').get_attribute("ng-href")
			citeds_str += "," + cited_url
			cited_urls.append(cited_url)

			cited_paper = Table_papers()

			cited_paper.authors, cited_paper.title, cited_paper.conference, cited_date = self.parse_citing(el.find_element_by_css_selector('div[ng-bind-html="::item.displayText"]').text)
			cited_paper.published = self.convert_date_of_publication_to_datetime(cited_date)
			cited_paper.url = cited_url
			cited_paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			cited_papers.append(cited_paper)
			self.log.debug("cited_paper.title: " + cited_paper.title)
			self.log.debug("cited_paper: " + cited_paper.get_vars())

		self.move_to_paper_initial_page(driver, initial_url)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return " + citeds_str.lstrip(","))
		return citeds_str.lstrip(","), cited_papers, cited_urls


	def continuous_pushing_more_view_button(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		elements = driver.find_elements_by_css_selector('div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]')
		num_of_viewing = len(elements)
		limit_of_view = self.conf.getconf("IEEE_citation_num_at_first_page")
		self.log.debug("num_of_viewing[" + str(num_of_viewing) + "], limit_of_view[" + str(limit_of_view) + "]")

		while num_of_viewing > limit_of_view - 10:
			limit_of_view += self.conf.getconf("IEEE_citation_num_per_more_view")
			try:
				load_more_button = driver.find_element_by_xpath('//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]')
				load_more_button.click()
				driver.wait_appearance_of_tag(by="xpath", tag='//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]/span[@aria-hidden="false"]', timeout=num_of_viewing/2)
			except ElementNotVisibleException as e:
				self.log.debug("caught " + e.__class__.__name__ + " at loading more cited pages(" + str(limit_of_view) + ") paper[" + driver.current_url + "].")
				self.log.debug("there is no more paper. return current elements.")
				elements = driver.find_elements_by_css_selector('div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]')
				return elements
			except (TimeoutException, NoSuchElementException) as e:
				self.log.warning("caught " + e.__class__.__name__ + " at loading more cited pages(" + str(limit_of_view) + ") paper[" + driver.current_url + "].")
				driver.save_current_page("../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", driver.current_url) + ".png")
				driver.save_current_page("../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", driver.current_url) + ".html")

			elements = driver.find_elements_by_css_selector('div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]')
			num_of_viewing = len(elements)
			self.log.debug("num_of_viewing[" + str(num_of_viewing) + "], limit_of_view[" + str(limit_of_view) + "]")

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return elements


	def get_conference(self, driver):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		try:
			conference = driver.find_element_by_xpath('//div[@class="u-pb-1 stats-document-abstract-doi ng-scope"]')\
							.find_element_by_tag_name('a').text
			return conference
			self.log.debug("return: " + conference)
		except NoSuchElementException:
			self.log.debug("caught NoSuchElementExceptionatdate at get_conference. return \"\"")
			return ""

	def get_conference_and_urls_of_papers_in_same_conference(self, driver, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url
		#driver.save_current_page("../../var/ss/conferenced_paper_initial_page.png")
		#driver.save_current_page("../../var/ss/conferenced_paper_initial_page.html")
		if not driver.wait_appearance_of_tag(by="xpath", tag='//div[@class="u-pb-1 stats-document-abstract-publishedIn ng-scope"]', warning_messages=False):
			self.log.debug("no conference on paper page: " + initial_url)
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return \"\", []")
			return "", []

		element = driver.find_element_by_xpath('//div[@class="u-pb-1 stats-document-abstract-publishedIn ng-scope"]')
		conference = element.find_element_by_xpath("a").text
		self.log.debug("conference: " + str(conference))
		conference_url = element.find_element_by_xpath("a").get_attribute("href")
		self.log.debug("conference_url: " + str(conference_url))

		driver.get(conference_url)
		if not self.wait_conference_page(driver, timeout):
			self.log.debug("cannot read conferencepage: " + conference_url)
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return conference[" + str(conference) + ", []")
			return conference, []

		urls_in_conference = self.get_urls_of_papers_in_conference(driver, num_of_papers, timeout)
		#driver.save_current_page("../../var/ss/conferenced_paper_conference_page.png")
		#driver.save_current_page("../../var/ss/conferenced_paper_conference_page.html")
		
		self.move_to_paper_initial_page(driver, initial_url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return conference[" + str(conference) + "], urls_in_conference: " + str(urls_in_conference))
		return conference, urls_in_conference
		

	def get_date_of_publication(self, driver):
		#Date of Publication: 06 January 200 or Date of Conference 14-16 Nov. 2006
		try:
			date = driver.find_element_by_xpath('//div[@ng-if="::vm.details.isJournal == true"]').text
			return self.convert_date_of_publication_to_datetime(date)
		except NoSuchElementException:
			try:
				date = driver.find_element_by_xpath('//div[@ng-if="::vm.details.isConference == true"]').text
				return self.convert_date_of_publication_to_datetime(date)
			except NoSuchElementException:
				self.log.debug("caught NoSuchElementException. date = None") ##todo get from paper??
				driver.save_current_page("./samples/caughtNoSuchElementExceptionatdate_of_publication.png")
				driver.save_current_page("./samples/caughtNoSuchElementExceptionatdate_of_publication.html")
				return None


	def create_driver(self, url="", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("url[" + url + "]")

		if url == "":
			url = self.conf.getconf("IEEE_top_page")

		driver = PhantomJS_(desired_capabilities={'phantomjs.page.settings.resourceTimeout': timeout})

		if url == self.conf.getconf("IEEE_top_page"):
			self.log.debug("driver.get IEEE_top_page (" + url + "). wait start")
			driver.get(url, tag_to_wait='//li[@class="Media-articles-item"]', by="xpath", timeout=timeout)
			self.log.debug("driver.get finished")
		else:
			self.log.debug("driver.get(" + url + ")")
			driver.get(url)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return driver")
		return driver


	def move_to_paper_initial_page(self, driver, initial_url, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		driver.get(initial_url)
		driver.wait_appearance_of_tag(by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def wait_search_results(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		self.log.debug("Wait start.")
		try:
			tag = '//input[@type="checkbox" and @data-group="search-results-group" and @ng-checked="vm.allSelected()"]'
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_xpath(tag))
		except (TimeoutException, NoSuchElementException) as e:
			self.log.warning("caught" + e.__class__.__name__ + " at loading the keywords results page.")
			self.log.warning("at " + sys._getframe().f_code.co_name)
			self.log.warning("url[" + driver.current_url + "]")
			self.log.warning("tag[find_element_by_xpath(" + tag + ")")
			filename = "../../var/ss/TimeoutExceptionatLoadtheKeywordsResultsPage." + re.sub(r"/|:|\?", "", driver.current_url)
			driver.save_current_page(filename + ".png")
			driver.save_current_page(filename + ".html")
			self.log.warning(e, exc_info=True)
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return False")
			return False
		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return True")
		return True

	def wait_conference_page(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("Wait start.")
		if not driver.wait_appearance_of_tag(by="xpath", tag='//input[@type="hidden" and @name="submitAbsUrl" and @id="submitAbsUrl" and @value="/xpl/articleDetails.jsp"]'):
			self.log.warning("wait error at wait_conference_page. return False")
			return False

		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. return True")
		return True


	def wait_button_to_pdf_page(self, driver, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("Wait start.")
		try:
			WebDriverWait(driver, timeout).until(lambda driver: driver.find_element_by_css_selector('i[class="icon doc-act-icon-pdf"]'))
		except TimeoutException:
			self.log.warning("caught TimeoutException at waiting button which go to pdf page.")
		except NoSuchElementException:
			self.log.warning("caught NoSuchElementException at waiting button which go to pdf page.")
		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def download_a_paper(self, driver, path="../../data/tmp/", filename="default", timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = driver.current_url

		m = "downloading paper to " + path + ". title[" + filename + "]"
		self.log.info(m)
		print(m)

		self.wait_button_to_pdf_page(driver, timeout)

		retries = 10
		while retries > 0:
			try:
				button = driver.find_element_by_css_selector('i[class="icon doc-act-icon-pdf"]')
				button.click()
				self.log.debug("clicked button and no exception. break")
				break
			except (RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.log.warning("caught " + e.__class__.__name__ + " at click download pdf button. retries[" + str(retries) + "]")
				self.log.warning(e, exc_info=True)
				time.sleep(self.conf.getconf("IEEE_wait_time_per_download_paper"))
				driver.reconnect(initial_url)
				self.wait_button_to_pdf_page(driver, timeout)
				retries -= 1
			except NoSuchElementException as e:
				self.log.warning("caught " + e.__class__.__name__ + " at click download pdf button. retries[" + str(retries) + "]")
				self.log.warning(e, exc_info=True)
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
			self.log.warning("caught TimeoutException at load the iEEE pdf page.")
			self.log.warning("skip to download pdf. reuturn \"\"")
			driver.get(initial_url)
			return ""
		except NoSuchElementException:
			self.log.warning("caught NoSuchElementException at load the iEEE pdf page.")
			self.log.warning("skip to download pdf. reuturn \"\"")
			driver.get(initial_url)
			return ""
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
			self.log.warning("error at " + command)

		#self.save_current_page(driver, "./samples/7898372.png")
		#self.save_current_page(driver, "./samples/7898372.html")

		driver.get(initial_url)

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return[" + path + filename + "]")
		return path + filename


	def convert_date_of_publication_to_datetime(self, string):
		## If you want examples of conversion, please read
		##../../test_cases/scraping/IEEEXplore_test.py.test_convert_date_of_publication_to_datetime
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		if string == None:
			self.log.debug("string is None. return None")
			return None

		self.log.debug("string[" + string + "]")
		date = ""
		month = ""
		year = ""
		string = string.replace("\n", "")
		tmp = string.split(":")
		if len(tmp) != 2:
			self.log.warning("len(tmp) != 2. return None")
			self.log.warning("string[" + string + "]")
			return None
		if tmp[1].replace(" ", "") == "":
			self.log.debug("tmp[1] is null. return None")
			self.log.debug("string[" + string + "]")
			return None

		date_month_year = tmp[1].lstrip()
		self.log.debug("date_month_year[" + date_month_year + "]")
		tmp2 = date_month_year.split("-")
		if len(tmp2) >= 3:
			self.log.warning("len(tmp2) >= 3. return None")
			self.log.warning("string[" + string + "]")
			return None
		elif len(tmp2) == 2:
			if re.match("^\d{1,2}$", tmp2[0]):
				date = tmp2[0]
			elif re.match("^\d{1,2}\s[a-zA-Z]", tmp2[0]):
				tmp3 = tmp2[0].split(" ")
				date = tmp3[0]
				month = tmp3[1].replace(".", "")

		tmp4 = date_month_year.split(" ")
		if len(tmp4) < 3:
			self.log.debug("only year")
			self.log.debug("string[" + string + "]")
			date = "1"
			month = "Jan"
		if date == "":
			date = tmp4[-3]
		if month == "":
			month = tmp4[-2].replace(".", "")
		if year == "":
			year = tmp4[-1]

		import datetime
		try:
			month = str(datetime.datetime.strptime(month, '%B').month)
		except ValueError:
			try:
				month = str(datetime.datetime.strptime(month, '%b').month)
			except ValueError:
				if month == "Sept":
					month = "9"
				else:
					self.log.warning("ValueError")
					self.log.warning("string:" + string)
					self.log.warning("month = 0")
					month = "0"

		self.log.debug("year[" + year + "], month[" + month + "], date[" + date + "]")

		timestamp = datetime.date(int(year), int(month), int(date))
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
		self.log.debug("src_str["+strings+"]")
		## If you want examples of conversion, please read
		##../../test_cases/scraping/IEEEXplore_test.py.test_parse_citing

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
		#self.log.debug("re.match(\"\d*\", " + year + ")")
		#year = re.match("*\d*",year).group() + "-01-01 00:00:00"
		#year += "-01-01 00:00:00"
		self.log.debug("citing year is none")
		year = None
		self.log.debug("authors[" + str(authors) + "], title[" + str(title) + "], conference[" + str(conference) + "], year[" + str(year) + "]")
		return authors, title, conference, year

	def parse_belonging(self, string):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.debug("src_str["+strings+"]")
		

	def set_options(self, driver, search_options, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##show" : "All Resul

		##PerPage" : "25"
		if search_options.PerPage != 25:
			try:
				element = driver.find_element_by_css_selector('div[ng-model="vm.rowsPerPage"] > div > select')
				Select(element).select_by_visible_text(str(search_options.PerPage))
				self.wait_search_results(driver, timeout)
			except NoSuchElementException:
				self.log.debug("caught NoSuchElementException at setting PerPage.")
				self.log.debug("No PerPage button means only hit a few papers.")
				self.log.debug("Nothing to do/")

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

		#self.save_current_page(driver, "./samples/after_set_options.png")
		#self.save_current_page(driver, "./samples/after_set_options.html")

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	## for debug
	def print_h2_attributes(self, driver):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		links = driver.find_elements_by_tag_name("h2")
		for link in links:
			print(link.text)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def save_current_page(self, driver, filename):
		self.log.warning(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.warning("this method will be removed.")
		self.log.warning("please use driver.save_current_page(filename)")

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
		self.opts.show_options()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


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
	
	def set_PerPage(self, int):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start. int[" + str(int) + "]")
		##10, 25,50,75,100
		if int <= 25:
			self.PerPage = 25
		elif int <= 50:
			self.PerPage = 50
		elif int <= 75:
			self.PerPage = 75
		else:
			self.PerPage = 100
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished. PerPage[" + str(self.PerPage) + "]")
		

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
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
