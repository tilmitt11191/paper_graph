#!/usr/bin/python
# -*- coding: utf-8 -*-

class Conf:
	def __init__(self):
		import yaml
		with open("../../etc/config.yml", "r") as f:
			conf = yaml.load(f)

		logfile = conf["logdir"] + conf["logfile"]
		loglevel = conf["loglevel"]
		import logging
		logging.basicConfig(filename=logfile, level=eval("logging."+loglevel))	
		self.log = logging.getLogger()

		
	@classmethod
	def getconf(cls, conf, conffile="../../etc/config.yml"):
		if(conffile==""):
			conffile="../../etc/config.yml"
		
		import yaml
		with open(conffile, "r") as f:
			confs = yaml.load(f)
		return confs[conf]





