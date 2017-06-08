
# -*- coding: utf-8 -*-


import unittest
import sys,os
import datetime
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log
from conf import Conf
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
from searchs import Searchs


class IEEEXplore_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.log = Log().getLogger()
		cls.conf = Conf()

		cls.log.info("\n\nIEEEXplore_test.setUpClass finished.\n---------- start ---------")

	def setUp(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
		from IEEEXplore import IEEEXplore as X
		self.xplore = X()

		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		from searchs import Searchs as s
		self.search = s()
	
	
	"""
	def test_get_attributes_spreading_of_target_paper_which_not_cited(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7921125/"
		url = "http://ieeexplore.ieee.org/document/891000"
		paper,\
			paper.url,\
			urls_of_papers_with_same_authors,\
			urls_of_papers_with_same_keywords,\
			citing_urls,\
			cited_urls,\
			urls_in_conference\
			= self.xplore.get_attributes_of_target_paper(url)
		self.assertEqual("Deep learning for texture classification via multi-wavelet fusion of scattering transforms", paper.title)
		self.assertEqual("Scattering,Wavelet transforms,Convolution,Machine learning,Databases,Shape,computer vision,texture classification,deep learning,wavelet,data fusion,scattering transform", paper.keywords)
		self.assertEqual("Amir Dadashnialehi,Alireza Bab-Hadiashar,Reza Hoseinnezhad", paper.authors)
		self.assertEqual("http://ieeexplore.ieee.org/document/6619007,http://ieeexplore.ieee.org/document/1615314,http://ieeexplore.ieee.org/document/5995635,http://ieeexplore.ieee.org/document/4394653,http://ieeexplore.ieee.org/document/4401927,http://ieeexplore.ieee.org/document/632179,http://ieeexplore.ieee.org/document/6706406,http://ieeexplore.ieee.org/document/4078016,http://ieeexplore.ieee.org/document/4669758,http://ieeexplore.ieee.org/document/5478671", paper.citings)
		self.assertEqual("", paper.citeds)
		self.assertEqual("Mechatronics (ICM), 2017 IEEE International Conference on", paper.conference)
		self.assertEqual(datetime.date(2017, 2, 13), paper.published)
		self.assertEqual("http://ieeexplore.ieee.org/document/7921125/", paper.url)
		self.assertEqual("../../data/tmp/Deeplearningfortextureclassificationviamulti-waveletfusionofscatteringtransforms.txt", paper.abstract_path)

		self.assertEqual(url, paper.url)
		print("urls_of_papers_with_same_authors: " + str(len(urls_of_papers_with_same_authors)))
		print("urls_of_papers_with_same_keywords", str(len(urls_of_papers_with_same_keywords)))
		print("citing_urls", str(len(citing_urls)))
		print("cited_urls", str(len(cited_urls)))
		print("urls_in_conference", str(len(urls_in_conference)))

		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_attributes_spreading_of_target_paper_which_cited_by_25(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/" 
		paper,\
			paper.url,\
			urls_of_papers_with_same_authors,\
			urls_of_papers_with_same_keywords,\
			citing_urls,\
			cited_urls,\
			urls_in_conference\
			= self.xplore.get_attributes_of_target_paper(url)
		#self.assertEqual("Deep learning for texture classification via multi-wavelet fusion of scattering transforms", paper.title)
		#self.assertEqual("Scattering,Wavelet transforms,Convolution,Machine learning,Databases,Shape,computer vision,texture classification,deep learning,wavelet,data fusion,scattering transform", paper.keywords)
		#self.assertEqual("Amir Dadashnialehi,Alireza Bab-Hadiashar,Reza Hoseinnezhad", paper.authors)
		#self.assertEqual("http://ieeexplore.ieee.org/document/6619007,http://ieeexplore.ieee.org/document/1615314,http://ieeexplore.ieee.org/document/5995635,http://ieeexplore.ieee.org/document/4394653,http://ieeexplore.ieee.org/document/4401927,http://ieeexplore.ieee.org/document/632179,http://ieeexplore.ieee.org/document/6706406,http://ieeexplore.ieee.org/document/4078016,http://ieeexplore.ieee.org/document/4669758,http://ieeexplore.ieee.org/document/5478671", paper.citings)
		#self.assertEqual("", paper.citeds)
		#self.assertEqual("Mechatronics (ICM), 2017 IEEE International Conference on", paper.conference)
		#self.assertEqual(datetime.date(2017, 2, 13), paper.published)
		#self.assertEqual("http://ieeexplore.ieee.org/document/7921125/", paper.url)
		#self.assertEqual("../../data/tmp/Deeplearningfortextureclassificationviamulti-waveletfusionofscatteringtransforms.txt", paper.abstract_path)

		self.assertEqual(url, paper.url)
		print("urls_of_papers_with_same_authors: " + str(len(urls_of_papers_with_same_authors)))
		print("urls_of_papers_with_same_keywords", str(len(urls_of_papers_with_same_keywords)))
		print("citing_urls", str(len(citing_urls)))
		print("cited_urls", str(len(cited_urls)))
		print("urls_in_conference", str(len(urls_in_conference)))

		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""


	"""
	def test_get_attributes_not_spreading_of_target_paper_which_not_cited(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7921125/"
		paper,\
			paper.url,\
			urls_of_papers_with_same_authors,\
			urls_of_papers_with_same_keywords,\
			citing_urls,\
			cited_urls,\
			urls_in_conference\
			= self.xplore.get_attributes_of_target_paper(url, spread_papers=False)
		self.assertEqual("Deep learning for texture classification via multi-wavelet fusion of scattering transforms", paper.title)
		self.assertEqual("Scattering,Wavelet transforms,Convolution,Machine learning,Databases,Shape,computer vision,texture classification,deep learning,wavelet,data fusion,scattering transform", paper.keywords)
		self.assertEqual("Amir Dadashnialehi,Alireza Bab-Hadiashar,Reza Hoseinnezhad", paper.authors)
		self.assertEqual("http://ieeexplore.ieee.org/document/6619007,http://ieeexplore.ieee.org/document/1615314,http://ieeexplore.ieee.org/document/5995635,http://ieeexplore.ieee.org/document/4394653,http://ieeexplore.ieee.org/document/4401927,http://ieeexplore.ieee.org/document/632179,http://ieeexplore.ieee.org/document/6706406,http://ieeexplore.ieee.org/document/4078016,http://ieeexplore.ieee.org/document/4669758,http://ieeexplore.ieee.org/document/5478671", paper.citings)
		self.assertEqual("", paper.citeds)
		self.assertEqual("Mechatronics (ICM), 2017 IEEE International Conference on", paper.conference)
		self.assertEqual(datetime.date(2017, 2, 13), paper.published)
		self.assertEqual("http://ieeexplore.ieee.org/document/7921125/", paper.url)
		self.assertEqual("../../data/tmp/Deeplearningfortextureclassificationviamulti-waveletfusionofscatteringtransforms.txt", paper.abstract_path)

		self.assertEqual(url, paper.url)
		self.assertEqual(0, len(urls_of_papers_with_same_authors))
		self.assertEqual(0, len(urls_of_papers_with_same_keywords))
		self.assertEqual(10, len(citing_urls))
		self.assertEqual(0, len(cited_urls))
		self.assertEqual(0, len(urls_in_conference))

		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_attributes_of_target_paper_for_bfs(self):
		# url = "http://ieeexplore.ieee.org/document/7130662/"
		#url = "http://ieeexplore.ieee.org/document/1055638/" # New directions in cryptography
		url = "http://ieeexplore.ieee.org/document/4773330"
		path = "../../data/tmp/"
		filename = "title"
		timeout = 30
		search = Searchs(initial_node=url, que=[url], times=1, visited=[], limit=100000)
		results = self.xplore.get_attributes_of_target_paper_for_bfs(
			search, path, filename, timeout)
		print("results: " + str(len(results)))
		print("2 authors: " + str(len(results[2])))
		print("3 keywords: " + str(len(results[3])))
		print("4 citings: " + str(len(results[4])))
		print("5 citeds: " + str(len(results[5])))
		print("6 conference: " + str(len(results[6])))
	"""
	"""
	def test_get_attributes_and_download_pdf_of_various(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		urls = []
		driver = PhantomJS_()
		#urls.append("http://ieeexplore.ieee.org/document/6517049") ##publish type error
		#urls.append("http://ieeexplore.ieee.org/document/7881332/") ##NoSuchWindowException
		#urls.append("http://ieeexplore.ieee.org/document/7312885/") ##Too long authors
		#urls.append("http://ieeexplore.ieee.org/document/7879258/") ##get paper page unfinised
		urls.append("http://ieeexplore.ieee.org/document/7888438/") ## open
		for url in urls:
			#driver = self.xplore.create_driver(url)
			self.search.node = url
			self.search.limit = len(urls)
			self.xplore.get_attributes_and_download_pdf(self.search, driver)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""

	def test_get_attributes_and_download_pdf_which_not_cited(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7849067/"
		driver = self.xplore.create_driver(url)
		self.search.node = url

		self.xplore.get_attributes_and_download_pdf(self.search, driver)

		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	def test_get_attributes_and_download_pdf_which_cited_by_25(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/" ##ElementNotVisibleException
		driver = self.xplore.create_driver(url)
		self.search.node = url
		self.xplore.get_attributes_and_download_pdf(self.search, driver)

		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	"""
	"""
	def test_get_attributes_and_download_pdf_which_cited_by_many(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##New directions in cryptography
		url = "http://ieeexplore.ieee.org/document/1055638/"

		driver = self.xplore.create_driver(url)
		self.search.node = url

		paper, paper.url, urls_of_papers_with_same_authors, urls_of_papers_with_same_keywords, citing_urls, cited_urls, urls_in_conference = self.xplore.get_attributes_and_download_pdf(self.search, driver)

		driver.close()
		print(paper.get_vars())
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""

	"""
	def test_get_papers_by_keywords_39hit(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords = "deep learning classification graph"
		self.xplore.get_papers_by_keywords(keywords)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_papers_by_keywords_333hit(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords = "\"edge computing\""
		from IEEEXplore import Search_options as opt
		opts = opt()
		opts.PerPage = 100

		self.xplore.get_papers_by_keywords(keywords,search_options=opts)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_papers_by_keywords_1549hit(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords = "deep learning classification"
		from IEEEXplore import Search_options as opt
		opts = opt()
		opts.PerPage = 100
		self.xplore.get_papers_by_keywords(keywords, num_of_papers="all", search_options=opts)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_urls_of_papers_in_search_results(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/search/searchresult.jsp?matchBoolean=true&queryText=%22Index%20Terms%22:.QT..QT.&newsearch=true" ## invalid search
		#url = "http://ieeexplore.ieee.org/search/searchresult.jsp?pageNumber=5&searchWithin=%22Authors%22:.QT.Joerg%20Kliewer.QT.&newsearch=true" ## 109hit
		#url = "http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=deep%20learning&newsearch=true" ##4868hit
		timeout=30
		driver = self.xplore.create_driver(url)
		self.xplore.get_urls_of_papers_in_search_results(driver, timeout=timeout)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_abstract(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7921125/"
		#url = "http://ieeexplore.ieee.org/document/1654301" # No abstract
		self.xplore.driver.get(url)
		print(self.xplore.get_abstract())

		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_authors_and_urls_of_papers_with_same_authors(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#url = "http://ieeexplore.ieee.org/document/4116687/"
		#url = "http://ieeexplore.ieee.org/document/1055638/"
		#url = "http://ieeexplore.ieee.org/document/7727082/"
		url = "http://ieeexplore.ieee.org/document/7914660/" # NoSuchElementException at authors loop, first author only one paper. and another error occurd in search by the author
		num_of_spreading_by_author = 
		#url = "http://ieeexplore.ieee.org/search/searchresult.jsp?searchWithin=%22Authors%22:.QT.Tamer%20Ba.AND..HSH.x015F;ar.QT.&newsearch=true"
		self.conf.getconf("IEEE_num_of_spreading_by_author")
		timeout=30
		driver = self.xplore.create_driver(url)
		authors_str, urls_of_papers_with_same_authors = self.xplore.get_authors_and_urls_of_papers_with_same_authors(driver, num_of_spreading_by_author, timeout)
		self.log.debug("authors_str[" + authors_str + "]")
		self.log.debug("len(urls_of_papers_with_same_authors)[" + str(len(urls_of_papers_with_same_authors)) + "]")
		self.log.debug("urls_of_papers_with_same_authors: " + str(urls_of_papers_with_same_authors))


		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_keywords_and_urls_of_papers_with_same_keywords(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/4116687/"
		"http://ieeexplore.ieee.org/document/7920294/" ## no keyword
		num_of_spreading_by_keyword = self.conf.getconf("IEEE_num_of_spreading_by_keyword")
		timeout=30
		driver = self.xplore.create_driver(url)
		keywords_str, urls_of_papers_with_same_keywords = self.xplore.get_keywords_and_urls_of_papers_with_same_keywords(driver, num_of_spreading_by_keyword, timeout)
		self.log.debug("keywords_str[" + keywords_str +"]")
		self.log.debug("len(urls_of_papers_with_same_keywords)[" + str(len(urls_of_papers_with_same_keywords)) + "]")
		self.log.debug("urls_of_papers_with_same_keywords: " + str(urls_of_papers_with_same_keywords))
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_citing_papers(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/"
		driver = self.xplore.create_driver(url)
		citings_str, citing_papers, citing_urls = self.xplore.get_citing_papers(driver)

		self.log.debug("citings_str[" + citings_str +"]")
		self.log.debug("len(citing_urls)[" + str(len(citing_urls)) + "]")
		self.log.debug("citing_urls: " + str(citing_urls))

		driver.close()

		self.assertEqual(citings_str, "http://ieeexplore.ieee.org/document/6563280,http://ieeexplore.ieee.org/document/6616116,http://ieeexplore.ieee.org/document/6108303,http://ieeexplore.ieee.org/document/6923535,http://ieeexplore.ieee.org/document/6226796,http://ieeexplore.ieee.org/document/6678114,http://ieeexplore.ieee.org/document/6184361,http://ieeexplore.ieee.org/document/7064907,http://ieeexplore.ieee.org/document/6257509,http://ieeexplore.ieee.org/document/1589108")
		self.assertEqual(len(citing_urls), 10)



		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""

	"""
	def test_get_cited_papers_which_not_cited(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7849067/"
		self.xplore.move_to_paper_top_page(url)

		citeds_str, cited_papers, cited_urls = self.xplore.get_cited_papers()
		self.log.debug("citeds_str[" + citeds_str +"]")
		self.log.debug("len(cited_urls)[" + str(len(cited_urls)) + "]")
		self.log.debug("cited_urls: " + str(cited_urls))

		self.assertEqual(citeds_str, "")
		self.assertEqual(len(cited_urls), 0)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	#url = "http://ieeexplore.ieee.org/document/4544774/" # cited by one

	def test_get_cited_papers_which_cited_by_27(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/"
		self.xplore.move_to_paper_top_page(url)

		citeds_str, cited_papers, cited_urls = self.xplore.get_cited_papers()
		#print("citeds_str[" + citeds_str +"]")
		#print("len(cited_urls)[" + str(len(cited_urls)) + "]")
		#print("cited_urls: " + str(cited_urls))
		self.xplore.driver.save_current_page("../../var/ss/cited_button_not_found.png")
		self.xplore.driver.save_current_page("../../var/ss/cited_button_not_found.html")

		self.assertEqual(citeds_str, "http://ieeexplore.ieee.org/document/7446253,http://ieeexplore.ieee.org/document/7564666,http://ieeexplore.ieee.org/document/7511367,http://ieeexplore.ieee.org/document/7247586,http://ieeexplore.ieee.org/document/7794956,http://ieeexplore.ieee.org/document/7842016,http://ieeexplore.ieee.org/document/7901477,http://ieeexplore.ieee.org/document/7794955,http://ieeexplore.ieee.org/document/7875428,http://ieeexplore.ieee.org/document/7841937,http://ieeexplore.ieee.org/document/7442079,http://ieeexplore.ieee.org/document/7517217,http://ieeexplore.ieee.org/document/7727082,http://ieeexplore.ieee.org/document/7536749,http://ieeexplore.ieee.org/document/7541539,http://ieeexplore.ieee.org/document/7792373,http://ieeexplore.ieee.org/document/7762913,http://ieeexplore.ieee.org/document/7542156,http://ieeexplore.ieee.org/document/7500395,http://ieeexplore.ieee.org/document/7727971,http://ieeexplore.ieee.org/document/7553459,http://ieeexplore.ieee.org/document/7555389,http://ieeexplore.ieee.org/document/7845499,http://ieeexplore.ieee.org/document/7572018,http://ieeexplore.ieee.org/document/7510809,http://ieeexplore.ieee.org/document/7552695")
		self.assertEqual(len(cited_urls), 26)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	"""
	"""
	def test_download_a_paper(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#url = "http://google.co.jp/"
		#url = "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7874313"
		#url = "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7898372"
		url = "http://ieeexplore.ieee.org/document/7898372/"
		path="../../data/tmp/"
		driver = self.xplore.create_driver(url)
		self.xplore.download_a_paper(driver, path)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_url_of_conference(self):
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#url = "http://ieeexplore.ieee.org/document/7130662/" # IEEE Transactions on Signal and Information Processing over Networks ( Volume: 1, Issue: 2, June 2015 )
		#url = "http://ieeexplore.ieee.org/document/1055638/" # IEEE Transactions on Information Theory ( Volume: 22, Issue: 6, Nov 1976 )
		url = "http://ieeexplore.ieee.org/document/7921125/" # 2017 IEEE International Conference on Mechatronics (ICM) 
		self.xplore.move_to_paper_top_page(url)
		conference_url = self.xplore.get_url_of_conference()
		print(conference_url)
		self.log.info(
			__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_conference_and_urls_of_papers_in_same_conference(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#url = "http://ieeexplore.ieee.org/document/7915547/" # has published in
		#url = "http://ieeexplore.ieee.org/document/1055638/" # has published in and decorated page
		## IET Renewable Power Generation.
		#url = "http://ieeexplore.ieee.org/document/7919059/"
		#url = "http://ieeexplore.ieee.org/document/7918696/" ## no next_button
		url = "http://ieeexplore.ieee.org/document/7130662/" ## IEEE Transactions on Signal and Information Processing over Networks ( Volume: 1, Issue: 2, June 2015 )

		num_of_spreading_by_conference = self.conf.getconf("IEEE_num_of_spreading_by_conference")
		timeout=30
		self.xplore.move_to_paper_top_page(url)

		conference, urls_of_papers_in_same_conference = self.xplore.get_conference_and_urls_of_papers_in_same_conference(num_of_spreading_by_conference, timeout)
		self.log.debug("conference[" + conference +"]")
		self.log.debug("len(urls_of_papers_in_same_conference)[" + str(len(urls_of_papers_in_same_conference)) + "]")
		self.log.debug("urls_of_papers_in_same_conference: " + str(urls_of_papers_in_same_conference))
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""


	def test_get_date_of_publication(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		urls = []
		#urls.append("http://ieeexplore.ieee.org/document/7914660/") ##Date of Publication: 28 April 2017
		#urls.append("http://ieeexplore.ieee.org/document/4773330/")
		#urls.append("http://ieeexplore.ieee.org/document/891000")
		urls.append("http://ieeexplore.ieee.org/document/117155") # 16-19 April 19906 ValueError: year is out of range


		for url in urls:
			self.xplore.move_to_paper_top_page(url)
			print(self.xplore.get_date_of_publication())


		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	"""
	def test_download_a_paper(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7849067/"
		driver = self.xplore.create_driver(url)
		self.search.node = url

		self.xplore.download_a_paper(driver, path="../../data/tmp/")
		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""

	"""
	def test_get_urls(self):
		import codecs
		with codecs.open('./samples/urls.txt', 'r', 'utf-8') as f:
			urls = f.read().strip().split("\n")
		driver = self.xplore.create_driver()
		for url in urls:
			self.log.debug("driver.get( "+url+")")
			driver.get(url)
	"""
	"""
	def test_convert_date_of_publication_to_datetime(self):
		##from
		##Date of Publication: 06 January 2016
		##to
		##2016-01-06
		##from
		##Date of Conference: 14-16 Nov. 2006
		##to
		##2006-11-14
		##from
		##Date of Conference: 27 June-2 July 2016
		##to
		##2016-06-27
		##from
		##Date of Publication: N/A 2016
		##to
		##2016-01-01
		##Date of Publication:
		##to
		##None
		# from
		# ""
		# to
		# None


		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		#self.get_date_of_publications()
		#dates = open('./samples/dates.txt', 'r')

		dates = ["Date of Publication: 06 January 2016", \
					"Date of Conference: 14-16 Nov. 2006", \
					"Date of Conference: 27 June-2 July 2016",\
					"Date of Publication: N/A 2016",\
					"Date of Conference: 9-11 Jan. 2017",\
					"Date of Conference: 4-8 Sept. 2016",\
					"Date of Publication: "\
					]

		for date in dates:
			print(date.strip())
			print(str(self.xplore.convert_date_of_publication_to_datetime(date)))
		#dates.close()

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""

	"""
	def test_convert_path_to_url(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = self.xplore.convert_path_to_url("http://ieeexplore.ieee.org/document/7874313/")
		self.assertEqual("http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7874313", url)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_parse_citing(self):
		#from
		#Daniel Garant, Wei Lu, "Mining Botnet Behaviors on the Large-Scale Web Application Community", Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on, pp. 185-190, 2013.
		#to
		#Daniel Garant, Wei Lu,
		#Mining Botnet Behaviors on the Large-Scale Web Application Community
		#Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on
		#pp. 185-190, 2013
		
		# from
		# IEEE Std 1363.2-2008, pp. 1-127, 2009
		# to
		# "", "", "", ""
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		text = "Daniel Garant, Wei Lu, \"Mining Botnet Behaviors on the Large-Scale Web Application Community\", Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on, pp. 185-190, 2013."
		authors, cited_title, cited_conference, cited_date = self.xplore.parse_citing(text)
		self.assertEqual("Daniel Garant, Wei Lu, ", authors)
		self.assertEqual("Mining Botnet Behaviors on the Large-Scale Web Application Community", cited_title)
		self.assertEqual(" Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on", cited_conference)
		#self.assertEqual("2013-01-01", cited_date)

		text = "Jianliang Zheng, M.J. Lee, M. Anshel, \"Toward Secure Low Rate Wireless Personal Area Networks\", Mobile Computing IEEE Transactions on, vol. 5, pp. 1361-1373, 2006, ISSN 1536-1233."
		authors, cited_title, cited_conference, cited_date = self.xplore.parse_citing(text)
		self.assertEqual("Jianliang Zheng, M.J. Lee, M. Anshel, ", authors)
		self.assertEqual("Toward Secure Low Rate Wireless Personal Area Networks", cited_title)
		self.assertEqual(" Mobile Computing IEEE Transactions on", cited_conference)
		#self.assertEqual("2006-01-01", cited_date)

		text = "IEEE Std 1363.2-2008, pp. 1-127, 2009"
		authors, cited_title, cited_conference, cited_date = self.xplore.parse_citing(text)
		print(authors)
		print(cited_title)
		print(cited_conference)
		print(str(cited_date))
		

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_continuous_pushing_more_view_button(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/citations?anchor=anchor-paper-citations-ieee&ctx=citations"
		driver = self.xplore.create_driver(url)
		self.xplore.save_current_page(driver, "./samples/before_continuous_pushing.html")
		self.xplore.save_current_page(driver, "./samples/before_continuous_pushing.png")
		self.xplore.continuous_pushing_more_view_button(driver)
		self.xplore.save_current_page(driver, "./samples/after_continuous_pushing.html")
		self.xplore.save_current_page(driver, "./samples/after_continuous_pushing.png")
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_get_papers_of_new_conferences(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.xplore.get_papers_of_new_conferences(10)
	"""
	"""
	def get_date_of_publications(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords="\"edge computing\""
		num_of_papers = "all"
		timeout = 10
		from IEEEXplore import Search_options as opt
		opts = opt()
		opts.PerPage = 100
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
		from phantomjs_ import PhantomJS_
		driver = PhantomJS_(desired_capabilities={'phantomjs.page.settings.resourceTimeout': timeout})
		driver.set_page_load_timeout(timeout)
		import codecs
		#self.xplore.search_by_keywords(driver, keywords, search_options=opts, timeout=timeout)
		#urls = self.xplore.get_urls_of_papers_in_keywords_page(driver, opts.PerPage, num_of_papers=num_of_papers, timeout=timeout)
		#with codecs.open('./samples/urls.txt', 'w', 'utf-8') as f:
		#	for url in urls:
		#		f.write(url + "\n")
		with codecs.open('./samples/urls.txt', 'r', 'utf-8') as f:
			urls = f.read().strip().split("\n")

		dates = []
		for url in urls:
			self.log.debug("driver.get( "+url+")")
			driver.get(url, by="xpath", tag_to_wait='//div[@ng-repeat="article in vm.contextData.similar"]', timeout=timeout)
			dates.append(self.xplore.get_date_of_publication(driver))
		import codecs
		with codecs.open('./samples/dates.txt', 'w', 'utf-8') as f:
			for date in dates:
				print(date)
				f.write(str(date) +"\n")

		return dates

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_breadth_first_search_by_get_attributes_and_download_pdf(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords="\"edge computing\""
		num_of_papers = 10
		path="../../data/tmp/"
		filename = "tmp.pdf"
		timeout=30

		all_citing_urls = ["http://ieeexplore.ieee.org/document/6324382", "http://ieeexplore.ieee.org/document/7881332/"]
		all_cited_urls = ["http://ieeexplore.ieee.org/document/7814490/",
		"http://ieeexplore.ieee.org/document/7780942/"]
		
		self.log.debug("all_citing_urls[" + str(len(all_citing_urls)) + "]")
		self.log.debug("all_cited_urls[" + str(len(all_cited_urls)) + "]")

		all_citing_urls.extend(all_cited_urls)
		
		driver = self.xplore.create_driver()
		search = Searchs(que=all_citing_urls, limit=num_of_papers, times=0)
		Searchs.breadth_first_search(search, [2, 3, 4, 5, 6], self.xplore.get_attributes_and_download_pdf, driver, path, filename)

		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
	"""
	def test_show_options(self):
		self.log.info("test_show_options start")
		print("default")
		self.xplore.show_options()
		print("35")
		self.xplore.opts.set_PerPage(35)
		self.xplore.show_options()
		print("75")
		self.xplore.opts.set_PerPage(75)
		self.xplore.show_options()
		print("1000")
		self.xplore.opts.set_PerPage(1000)
		self.xplore.show_options()
	"""
	"""
	def test_encode(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		string = "Tamer Başar"
		#string = re.sub(r'\b', "?", string)
		string = string.encode("utf-8", "replace")
		print(string)
		string = string.decode("utf-8", "replace")
		print(string)
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	"""
if __name__ == '__main__':
	unittest.main()
