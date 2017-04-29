
# -*- coding: utf-8 -*-


import unittest
import sys,os

class IEEEXplore_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
		from log import Log as l
		cls.log = l().getLogger()

		cls.log.info("\n\nIEEEXplore_test.setUpClass finished.\n---------- start ---------")
	
	def setUp(self):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
		from IEEEXplore import IEEEXplore as X
		self.xplore = X()
		
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		from searchs import Searchs as s
		self.search = s()
		

	"""
	def test_show_options(self):
		self.log.info("test_show_options start")
		self.xplore.show_options()
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
	def test_get_papers_by_keywords(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords = "\"edge computing\""
		num_of_papers = 1
		all_papers, all_cited_urls, all_citing_urls = self.xplore.get_papers_by_keywords(keywords, num_of_papers, timeout=30)
		print("all_papers[" + str(len(all_papers)) + "]")
		print("all_citing_urls[" + str(len(all_citing_urls)) + "]")
		self.log.debug("all_citing_urls:" + str(all_citing_urls))
		print("all_cited_urls[" + str(len(all_cited_urls)) + "]")
		self.log.debug("all_cited_urls:" + str(all_cited_urls))
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
			

	def test_get_urls_of_papers(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		driver = self.xplore.create_driver("http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=deep%20learning%20traffic")
		urls = self.xplore.get_urls_of_papers(driver, 1)
		print(str(urls))
		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def test_get_attributes_and_download_pdf_of_various(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		urls = []
		urls.append("http://ieeexplore.ieee.org/document/6517049") ##publish type error
		urls.append("http://ieeexplore.ieee.org/document/7881332/") ##NoSuchWindowException
		urls.append("http://ieeexplore.ieee.org/document/7312885/") ##Too long authors
		for url in urls:
			driver = self.xplore.create_driver(url)
			self.search.node = url
			self.search.limit = 1
			self.xplore.get_attributes_and_download_pdf(self.search, driver)
		
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")


	def test_get_attributes_and_download_pdf_which_cited_by_25(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7130662/" ##ElementNotVisibleException
		driver = self.xplore.create_driver(url)
		self.search.node = url
		self.xplore.get_attributes_and_download_pdf(self.search, driver)
		
		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	
	def test_get_attributes_and_download_pdf_which_not_cited(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/7849067/"
		driver = self.xplore.create_driver(url)
		self.search.node = url
			
		self.xplore.get_attributes_and_download_pdf(self.search, driver)
		
		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	
	
	def test_get_attributes_and_download_pdf_which_cited(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		url = "http://ieeexplore.ieee.org/document/4116687/"
		driver = self.xplore.create_driver(url)
		#driver = self.xplore.create_driver("./samples/paper_page.html")
		self.search.node = url
		self.xplore.get_attributes_and_download_pdf(self.search, driver)
		
		driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")
	

	def test_get_attributes_and_download_pdf_which_cited_by_many(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		##New directions in cryptography
		url = "http://ieeexplore.ieee.org/document/1055638/"
		
		driver = self.xplore.create_driver(url)
		self.search.node = url

		self.xplore.get_attributes_and_download_pdf(self.search, driver)
		
		driver.close()
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
	def get_date_of_publications(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords="\"edge computing\""
		num_of_papers = "all"
		timeout = 30
		from IEEEXplore import Search_options as opt
		opts = opt()
		opts.PerPage = 100
		driver = self.xplore.create_driver()
		self.xplore.search_by_keywords(driver, keywords, search_options=opts, timeout=timeout)
		urls = self.xplore.get_urls_of_papers_in_keywords_page(driver, opts.PerPage, num_of_papers=num_of_papers, timeout=timeout)
		dates = []
		for url in urls:
			driver.get(url)
			self.xplore.move_to_paper_initial_page(driver, url, timeout=timeout)
			dates.append(self.xplore.get_date_of_publication(driver))
		with codecs.open('./samples/dates.txt', 'w', 'utf-8') as f:
			for date in dates:
				print(date)
				f.write(date)
		
		return dates
			
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished")

	def test_convert_date_of_publication_to_datetime(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		self.get_date_of_publications()
		for date in open('./samples/dates.txt', 'r'):
			print(date)
			self.xplore.convert_date_of_publication_to_datetime(date)
			
		
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
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		str = "Daniel Garant, Wei Lu, \"Mining Botnet Behaviors on the Large-Scale Web Application Community\", Advanced Information Networking and Applications Workshops (WAINA) 2013 27th International Conference on, pp. 185-190, 2013."
		authors, cited_title, cited_conference, cited_date = self.xplore.parse_citing(str)
		print(authors)
		print(cited_title)
		print(cited_conference)
		print(cited_date)
		
		str = "Jianliang Zheng, M.J. Lee, M. Anshel, \"Toward Secure Low Rate Wireless Personal Area Networks\", Mobile Computing IEEE Transactions on, vol. 5, pp. 1361-1373, 2006, ISSN 1536-1233."
		authors, cited_title, cited_conference, cited_date = self.xplore.parse_citing(str)
		print(authors)
		print(cited_title)
		print(cited_conference)
		print(cited_date)
		
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
	def test_breadth_first_search_by_get_attributes_and_download_pdf(self):
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
		keywords="\"edge computing\""
		num_of_papers = 2
		path="../../data/tmp/"
		filename = "tmp.pdf"
		timeout=30
		
		#all_citing_urls = ["http://ieeexplore.ieee.org/document/7833471/", "http://ieeexplore.ieee.org/document/7820341/"]
		all_citing_urls = ["http://ieeexplore.ieee.org/document/6324382", "http://ieeexplore.ieee.org/document/7881332/"]
		driver = self.xplore.create_driver()
		
		sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/math")
		from searchs import Searchs
		search = Searchs(que=all_citing_urls, limit=num_of_papers, times=4)
		
		Searchs.breadth_first_search_with_class(search, 1, self.xplore.get_attributes_and_download_pdf, driver, path, filename)
		
		#driver.close()
		self.log.info(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
	"""
if __name__ == '__main__':
	unittest.main()

