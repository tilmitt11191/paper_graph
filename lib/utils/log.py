
# -*- coding: utf-8 -*-
"""
import logging
class myLogger(logging):
	def __init__(self):
		super()
"""

class Log:

	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		from conf import Conf

		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		loglevel = Conf.getconf("loglevel", conffile=conffile)
		rotate_log_size = Conf.getconf("rotate_log_size")

		import logging, logging.handlers
		logger = logging.getLogger()
		
		if len(logger.handlers) < 1:
			#fh = logging.FileHandler(filename="../../var/log/log2")
			#logger.addHandler(fh)
			rfh = logging.handlers.RotatingFileHandler(
				filename=logfile,
				maxBytes=rotate_log_size, 
				backupCount=Conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			logger.addHandler(rfh)

		#logging.basicConfig(filename="../../var/log/log2")

		id_ = id(logger)
		logger.setLevel(eval("logging."+loglevel))
		logger.info("return logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
		return logger













