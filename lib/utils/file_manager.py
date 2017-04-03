#!/usr/bin/python
# -*- coding: utf-8 -*-

class File_manager:
	def __init__(self):
		import yaml
		with open("../../etc/config.yml", "r") as f:
			conf = yaml.load(f)

		logfile = conf["logdir"] + conf["logfile"]
		loglevel = conf["loglevel"]	
		import logging
		logging.basicConfig(filename=logfile, level=eval("logging."+loglevel))	
		self.log = logging.getLogger()
		
		self.num_of_max_line = conf["num_of_max_line"]

		self.output_file_number = 0
		self.output_filename = ""
		self.output_codec = ""

	@classmethod
	def getconf(cls, conf, conffile="../../etc/config.yml"):
		if(conffile==""):
			conffile="../../etc/config.yml"
		
		import yaml
		with open(conffile, "r") as f:
			confs = yaml.load(f)
		return confs[conf]
	
	
	def set_output_filename(self, output_filename, suffix="csv"):
		self.output_filename = output_filename + "_" + str(self.output_file_number) + "." + suffix
	
	def renew_output_filename(self):
		self.log.info("renew_output_filename start")
		self.log.debug("previous filename[" + self.output_filename + "]")
		tmp = self.output_filename.split("_")
		self.output_filename = ""
		
		number_and_suffix = tmp[-1].split(".") # ex: ***_0.csv
		suffix = number_and_suffix[-1]
		tmp.pop()

		for s in tmp:
			self.output_filename += s + "_"
		#self.output_filename = self.output_filename[:-1]
		self.output_filename += str(self.output_file_number) + "." + suffix
		self.log.debug("following filename[" + self.output_filename + "]")
	
	
	def initialize_output_file(self, output_filename, suffix="csv", output_codec="utf-8"):
		self.log.info("initialize_output_file start. output_filename[" + output_filename + "], suffix[" + suffix + "], codec[" + output_codec + "]")
		self.set_output_filename(output_filename, suffix=suffix)
		self.output_codec = output_codec
		self.log.debug("renew output_filename to [" + self.output_filename + "]")

	
	def add_array_to_file(self, arr):
		self.log.info("add_array_to_file start.")
		import os.path
		if os.path.exists(self.output_filename):
			self.log.debug("self.num_of_max_line:"+str(self.num_of_max_line))
			import codecs
			f = codecs.open(self.output_filename, "r", self.output_codec)
			line_num=sum(1 for line in f)
			f.close()
		else:
			line_num = 0
		self.log.debug("line_num:" + str(line_num))

		while os.path.exists(self.output_filename) and line_num > self.num_of_max_line:
			self.output_file_number += 1
			self.renew_output_filename()
			
			self.log.debug("output_filename[{self.output_filename}]".format(**locals()))
		
		import codecs
		self.log.debug("write to [{self.output_filename}]".format(**locals()))
		with codecs.open(self.output_filename, 'a', self.output_codec) as f:
			for el in arr:
				f.write(el +"\n")
		
		return []
		self.log.info("add_array_to_file finished. return empty arr.")		


	
	def AAAAadd_array_to_file(self, arr, file, suffix="csv", codec="shift-jis"):
		self.log.info("AAAAadd_array_to_file start.")
		self.log.debug("file[{file}], suffix[{suffix}], codec[{codec}], num_of_max_line[{self.num_of_max_line}]".format(**locals()))
		self.log.debug("arr[arr]".format(**locals()))
		
		self.set_output_filename(file, suffix=suffix)
		
		import os.path
		if os.path.exists(self.output_filename):
			self.log.debug("self.num_of_max_line:"+str(self.num_of_max_line))
			import codecs
			f = codecs.open(self.output_filename, "r", codec)
			line_num=sum(1 for line in f)
			f.close()
		else:
			line_num = 0
		self.log.debug("line_num:" + str(line_num))

		while os.path.exists(self.output_filename) and line_num > self.num_of_max_line:
			self.output_file_number += 1
			#self.output_filename = file + "_" + str(self.output_file_number) + "." + suffix
			self.set_output_filename(file, suffix=suffix)
			
			self.log.debug("output_filename[{output_filename}]".format(**locals()))
		
		import codecs
		self.log.debug("write to [{self.output_filename}]".format(**locals()))
		with codecs.open(self.output_filename, 'a', codec) as f:
			for el in arr:
				f.write(el +"\n")

		self.log.info("AAAAadd_array_to_file finished. return empty arr.")
		return []


























