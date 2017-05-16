# -*- coding: utf-8 -*-
"""IEEEXplore.py."""

import sys
import os
import time
import re
import datetime

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import \
	TimeoutException, \
	NoSuchElementException, \
	ElementNotVisibleException

from http.client import RemoteDisconnected
from urllib.request import URLError

sys.path.append(
	os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log

sys.path.append(
	os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_

sys.path.append(
	os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs

sys.path.append(
	os.path.dirname(os.path.abspath(__file__)) + "/../../lib/db")
from table_papers import Table_papers
from table_citations import Table_citations
from table_authors import Table_authors


class IEEEXplore:
	"""class IEEEXplore."""

	def __init__(self):
		"""init."""
		self.log = Log.getLogger()
		self.opts = Search_options()
		self.driver = self.create_driver()
		self.log.debug("class " + __class__.__name__ + " created.")

	def get_attributes_of_target_paper(
			self,
			target_paper_url,
			spread_papers=True,
			path="../../data/tmp/",
			filename="title",
			timeout=30):
		m = __class__.__name__ + "." + sys._getframe().f_code.co_name + " start"
		print(m)
		self.log.info(m)

		self.log.debug("move_to_paper_top_page")
		self.move_to_paper_top_page(target_paper_url, timeout=timeout)

		paper = Table_papers(title=self.get_title())

		# if this paper already downloaded recently, this paper had visited and skip.
		if paper.has_already_downloaded():
			self.log.debug(
				"paper.has_already_downloaded. return paper, paper.url, [], [], " +
				str(paper.get_citings_array()) + ", " +
				str(paper.get_citeds_array()) + ", []")
			return [
				paper, paper.url, [], [],
				paper.get_citings_array(), paper.get_citeds_array(), []]

		self.log.debug("get attributes of this paper")
		self.log.debug("get authors")
		if spread_papers:
			self.log.debug("spread papers by authors")
			paper.authors, urls_of_papers_with_same_authors =\
				self.get_authors_and_urls_of_papers_with_same_authors(
					num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_author"),
					timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.authors = self.get_authors()
			urls_of_papers_with_same_authors = []

		self.log.debug("get keywords")
		if spread_papers:
			self.log.debug("spread papers by keywords")
			paper.keywords, urls_of_papers_with_same_keywords = \
				self.get_keywords_and_urls_of_papers_with_same_keywords(
					num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_keyword"),
					timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.keywords = self.get_keywords()
			urls_of_papers_with_same_keywords = []

		self.log.debug("get citing papers")
		paper.citings, citing_papers, citing_urls = self.get_citing_papers(timeout)

		self.log.debug("get cited papers")
		paper.citeds, cited_papers, cited_urls = self.get_cited_papers(timeout)

		self.log.debug("get conference")
		if spread_papers:
			self.log.debug("spread papers by conference")
			paper.conference, urls_in_conference = \
				self.get_conference_and_urls_of_papers_in_same_conference(
					num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_conference"),
					timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.conference = self.get_conference()
			urls_in_conference = []

		paper.published = self.get_date_of_publication()
		paper.url = target_paper_url
		paper.abstract_path = self.get_abstract(
			path=path, filename=filename, timeout=30)
		paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
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

		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug(
			"return [paper[" + paper.title + "], " +
			"paper_url[" + paper.url + "], " +
			"urls_of_papers_with_same_authors[" +
			str(len(urls_of_papers_with_same_authors)) + "], " +
			"urls_of_papers_with_same_keywords[" +
			str(len(urls_of_papers_with_same_keywords)) + "], " +
			"citing_urls[" + str(len(citing_urls)) + "], " +
			"cited_urls[" + str(len(cited_urls)) +
			"urls_in_conference[" + str(len(urls_in_conference)) +
			"]]")
		return [
			paper,
			paper.url,
			urls_of_papers_with_same_authors,
			urls_of_papers_with_same_keywords,
			citing_urls,
			cited_urls,
			urls_in_conference]

	"""
	def get_attributes_and_download_pdf(
		self, search, driver, path="../../data/tmp/",
		filename="title", timeout=30):
		get_attributes_and_download_pdf.
		print(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		search.times += 1
		target_paper_url = search.node
		m = "url[" + str(target_paper_url) + "]\n" + \
			"times[" + str(search.times) + "], + "\
			"len(que)[" + str(len(search.que)) + "], " + \
			"limit[" + str(search.limit) + "]"
		print(m)
		self.log.info(m)

		self.move_to_paper_top_page(driver, target_paper_url)

		paper = Table_papers(title=self.get_title(driver))
		# if this paper already downloaded recently, this paper had visited and skip.
		if paper.has_already_downloaded():
			self.log.debug(
				"paper.has_already_downloaded. return paper, paper.url, [], [], " +
				str(paper.get_citings_array()) + ", " +
				str(paper.get_citeds_array()) + ", []")
			return [
				paper, paper.url, [], [],
				paper.get_citings_array(), paper.get_citeds_array(), []]

		self.log.debug("get attributes of this paper")
		self.log.debug("get authors")
		if search.times + len(search.que) <= search.limit:
			paper.authors, urls_of_papers_with_same_authors =\
				self.get_authors_and_urls_of_papers_with_same_authors(
					driver, num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_author"),
					timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.authors = self.get_authors(driver)
			urls_of_papers_with_same_authors = []

		self.log.debug("get keywords")
		if search.times + len(search.que) <= search.limit:
			paper.keywords, urls_of_papers_with_same_keywords = \
				self.get_keywords_and_urls_of_papers_with_same_keywords(
					driver, num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_keyword"),
					timeout=timeout)
		else:
			self.log.debug("no need to spread anymore")
			paper.keywords = self.get_keywords(driver)
			urls_of_papers_with_same_keywords = []

		self.log.debug("get citing papers")
		paper.citings, citing_papers, citing_urls = self.get_citing_papers(
			driver, timeout)

		self.log.debug("get cited papers")
		paper.citeds, cited_papers, cited_urls = self.get_cited_papers(
			driver, timeout)

		self.log.debug("get conference")
		if search.times + len(search.que) <= search.limit:
			paper.conference, urls_in_conference = \
				self.get_conference_and_urls_of_papers_in_same_conference(
					driver, num_of_papers=Conf.getconf("IEEE_num_of_spreading_by_conference"),
					timeout=timeout)
		else:
			paper.conference = self.get_conference(driver)
			urls_in_conference = []
		paper.published = self.get_date_of_publication(driver)
		paper.url = target_paper_url
		paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
		if filename == "title":
			filename = paper.title + ".pdf"
		paper.path = self.download_a_paper(
			driver, path=path, filename=filename, timeout=timeout)
		self.log.debug("download finished. wait start.")
		time.sleep(Conf.getconf("IEEE_wait_time_per_download_paper"))
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
			self.log.debug(
				"search finished. 0 < search.limit and search.times >= search.limit.")
			self.log.debug("return [paper, paper.url, [], [], [], [], []]")
			search.que = [search.node]
			return [paper, paper.url, [], [], [], [], []]
		elif search.times + len(search.que) > search.limit:
			self.log.debug("search.times + len(search.que) < search.limit")
			self.log.debug("no more spread")
			self.log.debug("return [paper, paper.url, [], [], [], [], []]")
			return [paper, paper.url, [], [], [], [], []]
		else:
			self.log.debug(
				__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
			self.log.debug(
				"return [paper[" + paper.title + "], paper_url[" + paper.url +
				"] citing_urls[" + str(citing_urls) + "] cited_urls[" + str(cited_urls) +
				"]]")
			return [
				paper,
				paper.url,
				urls_of_papers_with_same_authors,
				urls_of_papers_with_same_keywords,
				citing_urls,
				cited_urls,
				urls_in_conference]
	"""

	def get_papers_by_keywords(
		self, keywords, num_of_papers="all",
		search_options="default",
		path="../../data/tmp/", filename="title",
		timeout=30):
		"""get_papers_by_keywords."""
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.log.info(
			"keywords[" + keywords + "], num_of_papers[" + str(num_of_papers) + "]")

		if search_options == "default":
			search_options = Search_options()

		self.search_by_keywords(
			keywords, search_options=search_options, timeout=timeout)

		if num_of_papers == "all":
			tag = 'div[class="pure-u-1-1 Dashboard-header ng-scope"] > span'
			try:
				element = self.driver.find_element_with_handling_exceptions(
					by="CSS_SELECTOR", tag=tag, timeout=timeout, warning_messages=False)
				num_of_papers = int(element.text.split(" ")[-1].replace(",", ""))
			except NoSuchElementException as e:
				self.log.debug(
					"caught " + e.__class__.__name__ + " at get num_of_papers. set 100000")
				num_of_papers = 100000

		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")

		urls = self.get_urls_of_papers_in_search_results(
			num_of_papers, timeout)
		print("urls.size[" + str(len(urls)) + "]")

		all_papers = []
		all_urls_of_papers_with_same_authors = []
		all_urls_of_papers_with_same_keywords = []
		all_citing_urls = []
		all_cited_urls = []
		all_urls_in_conference = []

		search = Searchs(limit=num_of_papers)

		for url in urls:
			search.node = url
			[
				paper,
				paper_url,
				urls_of_papers_with_same_authors,
				urls_of_papers_with_same_keywords,
				citing_urls,
				cited_urls,
				urls_in_conference
			] = self.get_attributes_and_download_pdf(
				search, path=path, filename=filename)
			all_papers.append(paper)
			all_urls_of_papers_with_same_authors.extend(
				urls_of_papers_with_same_authors)
			all_urls_of_papers_with_same_keywords.extend(
				urls_of_papers_with_same_keywords)
			all_citing_urls.extend(citing_urls)
			all_cited_urls.extend(cited_urls)
			all_urls_in_conference.extend(urls_in_conference)
			self.log.info(
				__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

		return\
			all_papers,\
			urls,\
			all_urls_of_papers_with_same_authors,\
			all_urls_of_papers_with_same_keywords,\
			all_citing_urls,\
			all_cited_urls,\
			all_urls_in_conference

	def get_papers_of_target_conference(self, conference_name):
		"""get_papers_of_target_conference."""
		pass

	def get_papers_of_new_conferences(self, conference_num):
		"""get_papers_of_new_conferences."""
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name +
			"(conference_num=" + str(conference_num) + ") start.")

	def search_by_keywords(
		self, keywords, search_options="default", timeout=30):
		"""search_by_keywords."""
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.driver.get("http://ieeexplore.ieee.org/Xplore/home.jsp")
		self.driver.wait_appearance_of_tag(
			by="name", tag='queryText', timeout=timeout)
		try:
			self.driver.find_element_with_handling_exceptions(
				by="NAME", tag='queryText', timeout=timeout).send_keys(keywords)
			submit_button = self.driver.find_element_with_handling_exceptions(
				by="CLASS_NAME", tag='Search-submit', timeout=timeout)
			self.driver.click(submit_button)
		except(Exception) as e:
			self.log.exception('[[EXCEPTON OCCURED]]: %s', e)
			sys.exit("[[EXCEPTON OCCURED]]please check logfile.")
		self.wait_search_results(timeout)

		self.set_options(search_options, timeout)

		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		return 0

	def get_urls_of_papers_in_search_results(
		self, num_of_papers="all", timeout=30):
		"""get_urls_of_papers_in_search_results."""
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.wait_search_results(timeout)
		self.log.debug("url:" + self.driver.current_url)

		if num_of_papers == "all":
			tag = 'div[class="pure-u-1-1 Dashboard-header ng-scope"] > span'
			element = self.driver.find_element_with_handling_exceptions(
				by="CSS_SELECTOR", tag=tag, timeout=timeout)
			results = element.text.split(" ")
			self.log.debug(
				"num of search result string[" + str(len(results)) + "]")
			if len(results) < 4:
				self.log.warning(
					"\n" + "url:" + self.driver.current_url + "\n" +
					"len(results) < 3 \n" +
					"no search result in this page?\n" +
					"return []")
				return []
			if results[3] == "1":
				num_of_papers = 1
			else:
				num_of_papers = int(results[-1].replace(",", ""))
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")

		self.opts.set_PerPage(num_of_papers)
		self.set_options(self.opts, timeout=timeout)

		urls = []
		visited_buttons = ["1"]

		while True:
			self.log.debug("get paper urls in current page")
			for i in range(self.opts.PerPage):
				tag = '//div[@class=' +\
					'"js-displayer-content u-mt-1 ' +\
					'stats-SearchResults_DocResult_ViewMore ng-scope hide"]'
				paper_elements = self.driver.find_elements_with_handling_exceptions(
					by="XPATH", tag=tag, timeout=timeout)
				self.log.debug(
					"scroll times[" + str(i) +
					"] len(paper_elements)[" + str(len(paper_elements)) + "]")
				self.driver.execute_script_with_handling_exceptions(
					"window.scrollTo(0, document.body.scrollHeight);")
				if len(paper_elements) == self.opts.PerPage:
					break
			self.log.debug(
				"len(paper_elements)[" + str(len(paper_elements)) + "]")

			for paper_element in paper_elements:
				url = paper_element.find_element_by_css_selector(
					'a').get_attribute("href")
				self.log.debug("url[" + url + "]")
				urls.append(url)
				if len(urls) >= num_of_papers:
					self.log.debug(
						"len(urls)[" + str(len(urls)) +
						"] > num_of_papers[" + str(num_of_papers) + "]. return urls.")
					return urls

			self.log.debug("search buttons to next page")
			tag = '//a[@href="" and @ng-click="selectPage(page.number) "' +\
				'and @class="ng-binding"]'
			buttons = self.driver.find_elements_with_handling_exceptions(
				by="XPATH", tag=tag, timeout=timeout)
			if len(buttons) <= 1:
				self.log.debug(
					"len(buttons)[" + str(len(buttons)) +
					"] <= 1. search results in only this page. break")
				break

			i = 0
			for button in buttons:
				self.log.debug(
					"i[" + str(i) + "], button.text[" +
					button.text + "], visited_buttons:" + str(visited_buttons))
				if button.text not in visited_buttons:
					next_button = button
					self.log.debug("break")
					break
				i += 1
			if i == len(buttons):
				self.log.debug(
					"i = len(buttons). already visited all buttons. break")
				break

			visited_buttons.append(next_button.text)
			self.log.debug("move to next page[" + next_button.text + "]")
			self.driver.click(next_button)
			self.wait_search_results(timeout)

		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name +
			" finished. return urls[" + str(len(urls)) + "]")
		return urls

	def get_urls_of_papers_in_conference(
		self, num_of_papers="all", timeout=30):
		"""get_urls_of_papers_in_conference."""
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = self.driver.current_url

		if num_of_papers == "all":
			tag = 'div[class="results-display"] > b'
			elements = self.driver.find_elements_with_handling_exceptions(
				by="CSS_SELECTOR", tag=tag, timeout=timeout, url=initial_url)
			if len(elements) == 2:
				num_of_papers = int(elements[1].text)
			else:
				self.log.warning("at get_urls_of_papers_in_conference")
				self.log.warning("num_of_papers == all and len(elements) != 2")
				filename = "../../var/ss/get_urls_of_papers_in_conference_len_not_equal_2"
				self.log.warning("save to " + filename)
				self.driver.save_current_page(filename + ".png")
				self.driver.save_current_page(filename + ".html")
				num_of_papers = 100000000000
		self.log.debug("num_of_papers[" + str(num_of_papers) + "]")

		self.opts.set_PerPage(num_of_papers)
		self.driver.get(
			self.driver.current_url + "&rowsPerPage=" + str(self.opts.PerPage))
		if not self.wait_conference_page(timeout):
			self.log.debug("cannot read conference page: " + conference_url)
			self.log.debug(
				__class__.__name__ + "." + sys._getframe().f_code.co_name +
				" finished. return []")
			return []

		urls = []
		visited_buttons = []
		while True:
			self.log.debug("get paper urls in current page")
			paper_elements = self.driver.find_elements_with_handling_exceptions(
				by="XPATH", tag='//h3/a', timeout=timeout)
			self.log.debug(
				"len(paper_elements)[" + str(len(paper_elements)) + "]")
			for el in paper_elements:
				urls.append(el.get_attribute("href"))
				if len(urls) >= num_of_papers:
					self.log.debug(
						"len(urls)[" + str(len(urls)) + "] >= num_of_papers[" + str(num_of_papers) + "]")
					self.driver.get(initial_url)
					self.wait_conference_page(timeout)
					self.log.debug(
						"get_urls_of_papers_in_conference finished. return urls: " + str(urls))
					return urls

			self.log.debug("search buttons to next page")
			try:
				tag = '//div[@class="pagination"]/a[@href="#" and ' +\
					'@aria-label="Pagination Next Page" and @class="next ir"]'
				next_button = self.driver.find_element_with_handling_exceptions(
					by="XPATH", tag=tag, 
					warning_messages=False, timeout=timeout)
			except NoSuchElementException as e:
				self.log.debug(
					"caught " + e.__class__.__name__ +
					" at get_urls_of_papers_in_conference.")
				self.log.debug(
					"This page does not have next button.url[" +
					self.driver.current_url + "]")
				self.log.debug("break")
				break

			next_button_attribute = next_button.get_attribute("onclick")
			if next_button_attribute in visited_buttons:
				self.log.debug("visited all button. break")
				break
			visited_buttons.append(next_button_attribute)
			self.log.debug("visited_buttons: " + str(visited_buttons))
			self.log.debug("move to next page[" + next_button_attribute + "]")
			self.driver.click(next_button)
			if not self.wait_conference_page(timeout):
				self.log.warning(
					"cannot read conference next page: " + self.driver.current_url)
				self.log.warning("break")
				break

		self.driver.get(initial_url)
		self.wait_conference_page(timeout)
		self.log.debug(
			"get_urls_of_papers_in_conference finished. return urls: " + str(len(urls)))
		return urls

	def get_title(self):
		"""get_title."""
		if not self.wait_paper_top_page():
			self.log.warning(
				__class__.__name__ + "." + sys._getframe().f_code.co_name)
			self.log.warning("failed to load paper top page")
			return False

		tag = '//div[@class="pure-g stats-document-header ng-scope"]' +\
			'/div/div[@class="document-title-container ng-binding"]' +\
			'/h1[@class="document-title"]' +\
			'/span[@ng-bind-html="vm.displayDocTitle"]'
		return self.driver.find_element_with_handling_exceptions(
			by="XPATH", tag=tag).text

	def get_abstract(self, path="../../data/tmp/",
		filename="title", timeout=30):
		"""get_abstract."""
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		if not self.wait_paper_top_page():
			self.log.warning(
				__class__.__name__ + "." + sys._getframe().f_code.co_name)
			self.log.warning("failed to load paper top page")
			return False

		if filename == "title":
			filename = self.get_title()
		filename = path + re.sub(r"\s|/|:|\?|\.", "", filename) + ".txt"

		tag = '//div[@class="pure-g"]/div/div/div[@class="abstract-text ng-binding"]'
		try:
			element = self.driver.find_element_with_handling_exceptions(
				by="XPATH", tag=tag, timeout=timeout)
		except NoSuchElementException as e:
			self.log.warning("caught " + e.__class__.__name__ + " at get_abstract")
			self.log.warning("url: " + self.driver.current_url)
			self.log.warning("return \"\"")
			return ""

		abstract = element.text

		f = open(filename, "w")
		f.write(abstract)
		f.close()

		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return filename")
		return filename

	def get_authors(self):
		"""get_authors."""
		authors_str = ""
		tag = '//span[@ng-bind-html="::author.name"]'
		elements = self.driver.find_elements_with_handling_exceptions(
			by="XPATH", tag=tag)

		for el in elements:
			authors_str += "," + el.text
		authors_str = authors_str.lstrip(",")
		return authors_str

	def get_authors_and_urls_of_papers_with_same_authors(
		self, num_of_papers="all", timeout=30):
		"""get_authors_and_urls_of_papers_with_same_authors."""
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = self.driver.current_url

		self.driver.wait_appearance_of_tag(
			by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')
		try:
			tag = '//span[@class="authors-info ng-binding ng-scope" and ' +\
				'@ng-repeat="author in vm.authors"]' +\
				'/span[@ng-if="::author.affiliation" or ' +\
				'@ng-if="::!author.affiliation"]/a'
			elements = self.driver.find_elements_with_handling_exceptions(
				by="XPATH", tag=tag, timeout=timeout, url=initial_url)
		except NoSuchElementException as e:
			self.log.warning("caught " + e.__class__.__name__ +
							 " at find authors elements.")
			self.log.warning(
				"Does this page have no author? please check url[" + self.driver.current_url + "]")
		self.log.debug("len(authors_elements)[" + str(len(elements)) + "]")

		authors_str = ""
		urls_of_authors = []
		urls_of_papers_with_same_authors = []

		for el in elements:
			author_name = el.find_element_by_xpath(
				'span[@ng-bind-html="::author.name"]').text
			self.log.debug("author_name[" + author_name + "]")
			if "," + author_name in authors_str:
				self.log.debug(
					"author_name[" + author_name + "] is deplicated. not add.")
			else:
				authors_str += "," + author_name
				author = Table_authors()
				author.name = author_name
				urls_of_authors.append(Conf.getconf(
					"IEEE_website") + el.get_attribute("ng-href"))
				belonging = el.get_attribute("qtip-text")
				author.belonging = belonging
				self.log.debug("author: " + author.get_vars())
				author.renewal_insert()
		authors_str = authors_str.lstrip(",")

		for link in urls_of_authors:
			self.driver.get(link)
			self.wait_search_results(timeout)
			urls_of_papers_with_same_authors.extend(
				self.get_urls_of_papers_in_search_results(num_of_papers, timeout))
		# delete duplicated elements
		urls_of_papers_with_same_authors = list(
			set(urls_of_papers_with_same_authors))

		self.move_to_paper_top_page(initial_url)
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		return authors_str, urls_of_papers_with_same_authors

	def get_keywords(self):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		# keywords
		keywords_str = ""
		tag = '//a[@ng-bind-html="::term"]'
		elements = self.driver.find_elements_with_handling_exceptions(by="XPATH", tag=tag)
		for el in elements:
			keyword = el.text
			if "," + keyword in keywords_str:
				self.log.debug(
					"keyword[" + keyword + "] is deplicated. not add.")
			else:
				keywords_str += "," + el.text
		keywords_str = keywords_str.lstrip(",")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return: " + keywords_str)
		return keywords_str

	def get_keywords_and_urls_of_papers_with_same_keywords(self, num_of_papers="all", timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		initial_url = self.driver.current_url
		self.driver.wait_appearance_of_tag(
			by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')
		try:
			tag = '//a[@ng-bind-html="::term"]'
			elements = self.driver.find_elements_with_handling_exceptions(by="XPATH", tag=tag, timeout=timeout, url=initial_url)
		except NoSuchElementException as e:
			self.log.warning("caught " + e.__class__.__name__ +
							 " at find keywords elements.")
			self.log.warning(
				"Does this page have no keyword? please check url[" + self.driver.current_url + "]")
		self.log.debug("len(keywords)[" + str(len(elements)) + "]")

		keywords_str = ""
		urls_of_keywords = []
		urls_of_papers_with_same_keywords = []

		for el in elements:
			keyword = el.text
			self.log.debug("keyword[" + keyword + "]")
			if "," + keyword in keywords_str:
				self.log.debug(
					"keyword[" + keyword + "] is deplicated. not add.")
			else:
				keywords_str += "," + keyword
				link = el.get_attribute("href")
				self.log.debug("link[" + link + "]")
				urls_of_keywords.append(link)
		keywords_str = keywords_str.lstrip(",")
		for link in urls_of_keywords:
			self.driver.get(link)
			self.wait_search_results(timeout)
			urls_of_papers_with_same_keywords.extend(
				self.get_urls_of_papers_in_search_results(num_of_papers, timeout))
		# delete duplicated elements
		urls_of_papers_with_same_keywords = list(
			set(urls_of_papers_with_same_keywords))

		self.move_to_paper_top_page(initial_url)
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		return keywords_str, urls_of_papers_with_same_keywords

	def get_citing_papers(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		citings_str = ""
		citing_papers = []
		citing_urls = []

		try:
			tag='div[ng-repeat="article in vm.contextData.similar"]'
			elements = self.driver.find_elements_with_handling_exceptions(by="CSS_SELECTOR", tag=tag, timeout=timeout)
		except NoSuchElementException:
			self.log.debug(
				"caught NoSuchElementException at get_citing_papers.")
			self.log.debug("this paper has no citing paper. retrun []")
			return citings_str, citing_papers, citing_urls
		self.log.debug("num of citings[" + str(len(elements)) + "]")

		self.log.debug("create arrays of paper and url")
		for el in elements:
			citing_paper = Table_papers()
			citing_paper.url = Conf.getconf(
				"IEEE_website") + el.find_element_by_css_selector('a').get_attribute("ng-href")
			citing_paper.title = el.find_element_by_css_selector(
				'a').get_attribute("title")
			citing_paper.authors = el.find_element_by_css_selector(
				'div[class="ng-binding"]').text.replace(";", ",")
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			self.log.debug("citing_paper.title: " + citing_paper.title)
			self.log.debug("citing_paper: " + citing_paper.get_vars())

			citings_str += "," + citing_paper.url
			citing_papers.append(citing_paper)
			citing_urls.append(citing_paper.url)
		citings_str = citings_str.lstrip(",")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		self.log.debug("return " + citings_str)
		return citings_str, citing_papers, citing_urls

	def get_cited_papers(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")

		citeds_str = ""
		cited_papers = []
		cited_urls = []

		initial_url = self.driver.current_url

		if not self.driver.wait_appearance_of_tag(
			by="xpath",
			tag='//button[@ng-if="::vm.document.metrics.citationCountPaper"]',
			warning_messages=False, retry=False, timeout=timeout):
			self.log.debug(
				"button not appeared. this paper not cited. return []")
			return citeds_str, cited_papers, cited_urls
		
		tag = '//a[@ng-click="vm.viewMoreRelated()"]'
		self.driver.get(
			self.convert_paper_url_to_cited_url(initial_url),
			tag_to_wait=tag, by="xpath")
		button = self.driver.find_element_with_handling_exceptions(
			by="XPATH", tag=tag)
		self.log.debug("click view all button")
		self.driver.click(button)
		tag = 'div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]'
		self.driver.wait_appearance_of_tag(
			by="css_selector", tag=tag, timeout=timeout)

		self.log.debug("continue pushing more view button")
		elements = self.continuous_pushing_more_view_button(timeout)
		self.log.debug("len(elements): " + str(len(elements)))

		self.log.debug("create arrays of papers and urls")
		for el in elements:
			cited_url = Conf.getconf("IEEE_website") + el.find_element_by_css_selector(
				'div[class="ref-links-container stats-citations-links-container"] > span > a').get_attribute("ng-href")
			citeds_str += "," + cited_url
			cited_urls.append(cited_url)

			cited_paper = Table_papers()

			cited_paper.authors, cited_paper.title, cited_paper.conference, cited_date = self.parse_citing(
				el.find_element_by_css_selector('div[ng-bind-html="::item.displayText"]').text)
			cited_paper.published = self.convert_date_of_publication_to_datetime(
				cited_date)
			cited_paper.url = cited_url
			cited_paper.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			cited_papers.append(cited_paper)
			self.log.debug("cited_paper.title: " + cited_paper.title)
			self.log.debug("cited_paper: " + cited_paper.get_vars())
		citeds_str = citeds_str.lstrip(",")
		self.move_to_paper_top_page(initial_url)

		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		self.log.debug("return " + citeds_str.lstrip(","))
		return citeds_str.lstrip(","), cited_papers, cited_urls

	def continuous_pushing_more_view_button(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")

		tag = 'div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]'
		elements = self.driver.find_elements_with_handling_exceptions(by="CSS_SELECTOR", tag=tag, timeout=timeout)
		num_of_viewing = len(elements)
		limit_of_view = Conf.getconf("IEEE_citation_num_at_first_page")
		self.log.debug("num_of_viewing[" + str(num_of_viewing) +
					   "], limit_of_view[" + str(limit_of_view) + "]")

		while num_of_viewing > limit_of_view - 10:
			limit_of_view += Conf.getconf(
				"IEEE_citation_num_per_more_view")
			try:
				tag = '//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]'
				load_more_button = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag, timeout=timeout)
				self.driver.click(load_more_button)
				self.driver.wait_appearance_of_tag(
					by="xpath", tag='//button[@class="load-more-button" and @ng-click="vm.loadMoreCitations(\'ieee\')"]/span[@aria-hidden="false"]', timeout=num_of_viewing / 2)
			except ElementNotVisibleException as e:
				self.log.debug("caught " + e.__class__.__name__ + " at loading more cited pages(" +
							   str(limit_of_view) + ") paper[" + self.driver.current_url + "].")
				self.log.debug(
					"there is no more paper. return current elements.")
				tag = 'div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]'
				elements = self.driver.find_elements_with_handling_exceptions(by="CSS_SELECTOR", tag=tag, timeout=timeout)
				return elements
			except (TimeoutException, NoSuchElementException) as e:
				self.log.warning("caught " + e.__class__.__name__ + " at loading more cited pages(" + str(
					limit_of_view) + ") paper[" + self.driver.current_url + "].")
				self.driver.save_current_page(
					"../../var/ss/" + e.__class__.__name__ + re.sub(r"/|:|\?|\.", "", driver.current_url) + ".png")
				self.driver.save_current_page("../../var/ss/" + e.__class__.__name__ + re.sub(
					r"/|:|\?|\.", "", self.driver.current_url) + ".html")

			tag = 'div[ng-repeat="item in vm.contextData.paperCitations.ieee"] > div[class="pure-g pushTop10"] > div[class="pure-u-23-24"]'
			elements = self.driver.find_elements_with_handling_exceptions(by="CSS_SELECTOR", tag=tag, timeout=timeout)
			num_of_viewing = len(elements)
			self.log.debug(
				"num_of_viewing[" + str(num_of_viewing) + "], limit_of_view[" + str(limit_of_view) + "]")

		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		return elements

	def get_url_of_conference(self, timeout=30):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

		# Check IEEE Transaction
		tag = '//span[@ng-if="::vm.details.issue" and @class="ng-scope"]/a'
		try:
			element = self.driver.find_element_with_handling_exceptions(
				by="XPATH", tag=tag,
				warning_messages=False)
			self.log.debug("element.text: " + element.text)
			url = element.get_attribute("href")
			self.log.debug("url: " + url)
			return url
		except Exception as e:
			self.log.debug("caught " + e.__class__.__name__)
			self.log.debug("this is not IEEE Transaction")

		tag = '//div[@class="u-pb-1 stats-document-abstract-publishedIn ng-scope"]'
		element = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag, timeout=timeout)
		conference = element.find_element_by_xpath("a").text
		self.log.debug("conference: " + str(conference))
		url = element.find_element_by_xpath("a").get_attribute("href")
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
		self.log.debug("return url: " + url)
		return url

	def get_conference(self):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		try:
			tag = '//div[@class="u-pb-1 stats-document-abstract-publishedIn ng-scope"]'
			conference = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag).find_element_by_tag_name('a').text
			return conference
			self.log.debug("return: " + conference)
		except NoSuchElementException:
			self.log.debug(
				"caught NoSuchElementExceptionatdate at get_conference. return \"\"")
			return ""

	def get_conference_and_urls_of_papers_in_same_conference(self, num_of_papers="all", timeout=30):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		initial_url = self.driver.current_url
		
		if not self.driver.wait_appearance_of_tag(by="xpath", tag='//div[@class="u-pb-1 stats-document-abstract-publishedIn ng-scope"]', warning_messages=False):
			self.log.debug("no conference on paper page: " + initial_url)
			self.log.debug(__class__.__name__ + "." +
						   sys._getframe().f_code.co_name + " finished. return \"\", []")
			return "", []
		conference_name = self.get_conference()
		conference_url = self.get_url_of_conference(timeout)
		self.log.debug("conference_url: " + str(conference_url))

		self.driver.get(conference_url)
		if not self.wait_conference_page(timeout):
			self.log.debug("cannot read conference page: " + conference_url)
			self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name +
						   " finished. return conference[" + str(conference) + ", []")
			return conference, []

		urls_in_conference = self.get_urls_of_papers_in_conference(
			num_of_papers, timeout)

		self.move_to_paper_top_page(initial_url)
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		self.log.debug(
			"return conference[" + conference_name + 
			": " + conference_url +
			"], urls_in_conference: " + str(urls_in_conference))
		return conference_name, urls_in_conference

	def get_date_of_publication(self):
		# Date of Publication: 06 January 200 or Date of Conference 14-16 Nov.
		# 2006
		try:
			tag = '//div[@ng-if="::vm.details.isJournal == true"]'
			date = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag, warning_messages=False).text
			return self.convert_date_of_publication_to_datetime(date)
		except NoSuchElementException:
			try:
				tag = '//div[@ng-if="::vm.details.isConference == true"]'
				date = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag, warning_messages=False).text
				return self.convert_date_of_publication_to_datetime(date)
			except NoSuchElementException:
				try:
					tag = '//div[@ng-if="::vm.details.isStandard == true"]'
					date = self.driver.find_element_with_handling_exceptions(by="XPATH", tag=tag, warning_messages=False).text
					return self.convert_date_of_publication_to_datetime(date)
				except:
					# todo get from paper??
					self.log.debug("caught NoSuchElementException. date = None")
					self.driver.save_current_page(
						"../../var/ss/caughtNoSuchElementExceptionatdate_of_publication.png")
					self.driver.save_current_page(
						"../../var/ss/caughtNoSuchElementExceptionatdate_of_publication.html")
				return None

	def create_driver(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		driver = PhantomJS_(desired_capabilities={
							'phantomjs.page.settings.resourceTimeout': timeout})
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return driver")
		return driver

	def move_to_paper_top_page(self, paper_top_url, timeout=30):
		self.log.debug(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.driver.get(paper_top_url)
		return self.wait_paper_top_page()

	def wait_paper_top_page(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		return self.driver.wait_appearance_of_tag(
			by="xpath", tag='//div[@ng-repeat=\"article in vm.contextData.similar\"]')

	def wait_search_results(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")

		self.log.debug("Wait start.")
		if self.driver.wait_appearance_of_tag(by="xpath", tag='//input[@type="checkbox" and @data-group="search-results-group" and @ng-checked="vm.allSelected()"]'):
			return False
		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return True")
		return True

	def wait_conference_page(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		self.log.debug("Wait start.")
		if not self.driver.wait_appearance_of_tag(by="xpath", tag='//input[@type="hidden" and @name="submitAbsUrl" and @id="submitAbsUrl" and @value="/xpl/articleDetails.jsp"]'):
			self.log.warning(
				"wait error at wait_conference_page. return False")
			return False

		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return True")
		return True

	def wait_button_to_pdf_page(self, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		self.log.debug("Wait start.")
		try:
			tag = 'i[class="icon doc-act-icon-pdf"]'
			self.driver.wait_appearance_of_tag(by="css_selector", tag=tag, timeout=timeout)
		except TimeoutException:
			self.log.warning(
				"caught TimeoutException at waiting button which go to pdf page.")
		except NoSuchElementException:
			self.log.warning(
				"caught NoSuchElementException at waiting button which go to pdf page.")
		self.log.debug("Wait Finished.")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")

	def download_a_paper(self, path="../../data/tmp/", filename="default", timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		initial_url = self.driver.current_url

		m = "downloading paper to " + path + ". title[" + filename + "]"
		self.log.info(m)
		print(m)

		self.wait_button_to_pdf_page(timeout)

		retries = 10
		while retries > 0:
			try:
				tag = 'i[class="icon doc-act-icon-pdf"]'
				button = self.driver.find_element_with_handling_exceptions(by="CSS_SELECTOR", tag=tag, timeout=timeout)
				self.driver.click(button)
				self.log.debug("clicked button and no exception. break")
				break
			except (RemoteDisconnected, ConnectionRefusedError, URLError) as e:
				self.log.warning("caught " + e.__class__.__name__ +
								 " at click download pdf button. retries[" + str(retries) + "]")
				self.log.warning(e, exc_info=True)
				time.sleep(Conf.getconf(
					"IEEE_wait_time_per_download_paper"))
				self.driver.reconnect(initial_url)
				self.wait_button_to_pdf_page(driver, timeout)
				retries -= 1
			except (NoSuchElementException, TimeoutException) as e:
				self.log.warning(\
					"caught " + e.__class__.__name__ + \
					" at click download pdf button. retries[" + str(retries) + "]")
				self.log.warning(e, exc_info=True)
				self.driver.save_current_page(\
					"../../var/ss/caught_" + e.__class__.__name__ + \
					"_at_click_download_pdf_button.html")
				self.driver.save_current_page(
					"../..//var/ss/caught_" + e.__class__.__name__ + \
					"_at_click_download_pdf_button.png")
				retries -= 1
		if retries == 0:
			self.log.error("driver.click(button) error at download_a_paper")
			self.log.error("retries == 0. please check url: " + self.driver.current_url)
			self.driver.save_current_page("../../var/ss/button_click_error.html")
			self.driver.save_current_page("../../var/ss/button_click_error.png")

		self.log.debug("Wait start.")
		try:
			tag = '//frameset[@rows="65,35%"]/frame'
			self.driver.wait_appearance_of_tag(by="xpath", tag=tag, timeout=timeout)
		except TimeoutException:
			self.log.warning(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name)
			self.log.warning(
				"caught TimeoutException at load the iEEE pdf page.")
			self.log.warning("skip to download pdf. reuturn \"\"")
			self.driver.get(initial_url)
			return ""
		except NoSuchElementException:
			self.log.warning(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name)
			self.log.warning(
				"caught NoSuchElementException at load the iEEE pdf page.")
			self.log.warning("skip to download pdf. reuturn \"\"")
			self.driver.get(initial_url)
			return ""
		self.log.debug("Wait Finished.")
		tag='//frameset[@rows="65,35%"]/frame'
		try:
			url = self.driver.find_elements_with_handling_exceptions(
				by="XPATH", tag=tag, timeout=timeout)[1].get_attribute("src")
		except (NoSuchElementException, IndexError) as e:
			self.log.warning(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name)
			self.log.warning("cannot get pdf url.")
			self.log.warning("paper url[" + initial_url + "]")
			self.driver.get(initial_url)
			return ""
		self.log.debug("url:" + url)

		if filename == "default":
			filename = url[:url.index("?")].split("/")[-1]
		filename = filename.replace(":", "")
		self.log.debug("filename:" + filename)
		command = "wget -p \"" + url + "\" -O \"" + \
			path + filename + "\" > /dev/null 2>&1"
		#command = "wget -p \"" + url + "\" -O \"" + path + filename + "\" 1> /dev/null 2>&1"
		#command = "wget -p \"" + url + "\" -O \"" + path + filename + "\""
		self.log.debug(command)
		try:
			self.log.debug(os.system(command))
		except:
			self.log.warning("error at " + command)

		self.driver.get(initial_url)

		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
		self.log.debug("return[" + path + filename + "]")
		return path + filename

	def convert_date_of_publication_to_datetime(self, string):
		# If you want examples of conversion, please read
		# ../../test_cases/scraping/IEEEXplore_test.py.test_convert_date_of_publication_to_datetime
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		if string == None or string == "":
			self.log.debug("string is None. return None")
			return None

		self.log.debug("string[" + string + "]")
		date = ""
		month = ""
		year = ""
		string = string.replace("\n", "")
		tmp = string.split(":")
		if len(tmp) != 2:
			self.log.warning("at " + sys._getframe().f_code.co_name)
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

		self.log.debug("year[" + year + "], month[" +
					   month + "], date[" + date + "]")

		self.log.debug("convert month[" + str(month) + "]")
		if month == "Sept":
			month = "9"
		elif month == "April":
			month = "4"
		else:
			try:
				month = str(datetime.datetime.strptime(month, '%B').month)
			except ValueError:
				try:
					month = str(datetime.datetime.strptime(month, '%b').month)
				except ValueError:
					self.log.warning("ValueError")
					self.log.warning("string:" + string)
					self.log.warning("month = 1")
					month = "1"

		if not re.match("^\d*$", date):
			date = "1"

		self.log.debug("year[" + year + "], month[" +
					   month + "], date[" + date + "]")

		timestamp = datetime.date(int(year), int(month), int(date))
		return timestamp

	def convert_paper_url_to_cited_url(self, url):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		# from
		# http://ieeexplore.ieee.org/document/4116687/?reload=true
		# to
		# http://ieeexplore.ieee.org/document/4116687/citations?anchor=anchor-paper-citations-ieee&ctx=citations
		self.log.debug("url[" + url + "]")
		converted_url = url.split(
			"?")[0] + "citations?anchor=anchor-paper-citations-ieee&ctx=citations"
		self.log.debug("converted_url[" + converted_url + "]")

		return converted_url

	def convert_paper_url_to_pdf_url(self, url):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		# from
		# http://ieeexplore.ieee.org/document/6324382/
		# to
		# http://ieeexplore.ieee.org/ielx7/35/7901458/07901477.pdf?tp=&arnumber=7901477&isnumber=7901458
		print("url[" + url + "]")

	def parse_citing(self, strings):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		self.log.debug("src_str[" + strings + "]")
		# If you want examples of conversion, please read
		# ../../test_cases/scraping/IEEEXplore_test.py.test_parse_citing

		array = strings.split("\"")
		if len(array) < 3:
			self.log.warning(__class__.__name__ + "." +
							 sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(array)(" + str(len(array)) +
							 ") < 3. return \"\", \"\", \"\", \"\"")
			return "", "", "", ""

		authors = array[0]
		title = array[1]
		new_array = array[2][1:].split(",")
		self.log.debug("new_array:" + str(new_array))
		self.log.debug(len(new_array))
		if len(new_array) < 3:
			self.log.warning(__class__.__name__ + "." +
							 sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(new_array)(" + str(len(new_array)) +
							 ") < 3. return authors, title, \"\", \"\"")
			return authors, title, "", ""

		elif len(new_array) == 3:
			conference, page, year = new_array
		elif len(new_array) == 4:
			conference, vol, page, year = new_array
		elif len(new_array) == 5:
			conference, vol, page, year, issn = new_array
		else:
			self.log.warning(__class__.__name__ + "." +
							 sys._getframe().f_code.co_name + " warning")
			self.log.warning("strings[" + strings + "]")
			self.log.warning("len(new_array)(" + str(len(new_array)) +
							 ") > 5. return authors, title, \"\", \"\"")
			return authors, title, "", ""
		#self.log.debug("re.match(\"\d*\", " + year + ")")
		#year = re.match("*\d*",year).group() + "-01-01 00:00:00"
		#year += "-01-01 00:00:00"
		self.log.debug("citing year is none")
		year = None
		self.log.debug("authors[" + str(authors) + "], title[" + str(title) +
					   "], conference[" + str(conference) + "], year[" + str(year) + "]")
		return authors, title, conference, year

	def parse_belonging(self, string):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		self.log.debug("src_str[" + strings + "]")

	def set_options(self, search_options, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		# show" : "All Resul"

		# PerPage" : "25"
		if search_options.PerPage != 25:
			try:
				tag = 'div[ng-model="vm.rowsPerPage"] > div > select'
				element = self.driver.find_element_with_handling_exceptions(
					by="CSS_SELECTOR", tag=tag, 
					warning_messages=False, timeout=timeout)
				Select(element).select_by_visible_text(
					str(search_options.PerPage))
				self.wait_search_results(timeout)
			except NoSuchElementException:
				self.log.debug(
					"caught NoSuchElementException at setting PerPage.")
				self.log.debug(
					"No PerPage button means only hit a few papers.")
				self.log.debug("Nothing to do")

		# Select(element).select_by_value("object:75")
		# SortBy" : "MostCit
		# ContentType" : "No
		# YearType" : "Range
		# YearFrom" : "1996"
		# YearTo" : "2017",
		# Year" : "2017",
		# Author" : "None",
		# Affiliation" : "No
		# PublicationTitle"
		# Publisher" : "None
		# ConferenceLocation

		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")

	# for breadth_first or depth_first searchs
	def get_attributes_of_target_paper_for_bfs(
		self, search, path, filename, timeout
		):
		target_paper_url = search.node
		m = "url[" + str(target_paper_url) + "]\n" + \
			"times[" + str(search.times) + "], "\
			"len(que)[" + str(len(search.que)) + "], " + \
			"limit[" + str(search.limit) + "]"
		print(m)
		self.log.info(m)

		if search.times + len(search.que) <= search.limit:
			spread_papers=True
		else:
			spread_papers=False
		
		results = self.get_attributes_of_target_paper(
				target_paper_url,
				spread_papers=spread_papers,
				path=path,
				filename=filename,
				timeout=timeout)

		search.times += 1
		wait_time = Conf.getconf("IEEE_wait_time_per_download_paper")
		self.log.debug("process finished. wait " + str(wait_time) + " seconds")
		time.sleep(wait_time)
		return results

	# for debug
	"""
	def save_current_page(self, filename):
		self.log.warning(__class__.__name__ + "." +
						 sys._getframe().f_code.co_name + " start")
		self.log.warning("this method will be removed.")
		self.log.warning("please use driver.save_current_page(filename)")

		path, suffix = os.path.splitext(filename)
		self.log.debug("path[" + path + "], suffix[" + suffix + "]")
		if suffix == ".html":
			f = open(filename, 'w')
			f.write(driver.page_source)
			f.close()
		elif suffix == ".png":
			driver.save_screenshot(filename)
		else:
			self.log.error("TYPEERROR suffix[" + suffix + "]")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
	"""
	def show_options(self):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		self.opts.show_options()
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")


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
		import sys
		import os
		sys.path.append(os.path.dirname(
			os.path.abspath(__file__)) + "/../lib/utils")
		from log import Log as l
		self.log = l.getLogger()

		self.log.debug("class " + __class__.__name__ + " created.")

	def set_PerPage(self, int):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start. int[" + str(int) + "]")
		##10, 25,50,75,100
		if int <= 25:
			self.PerPage = 25
		elif int <= 50:
			self.PerPage = 50
		elif int <= 75:
			self.PerPage = 75
		else:
			self.PerPage = 100

		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name +
					   " finished. PerPage[" + str(self.PerPage) + "]")

	def show_options(self):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		import inspect
		methods = []
		for method in inspect.getmembers(self, inspect.ismethod):
			methods.append(method[0])

		for var in self.__dir__():
			if not var.startswith("_") and var != "log" and not var in methods:
				print(var + "[" + str(eval("self." + var)) + "]")
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished")
