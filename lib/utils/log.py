#!/usr/bin/python
# -*- coding: utf-8 -*-

class Log:
	"""
	log = ""
	def __init__(self):
		from file_manager import File_manager as f
		f.getconf("loglevel", conffile=conffile)
		if(logfile==""):
			logfile = f.getconf("logdir", conffile=conffile) + f.getconf("logfile", conffile=conffile)
		loglevel = f.getconf("loglevel", conffile=conffile)
		rotate_log_size = f.getconf("rotate_log_size")

		import logging, logging.handlers
		
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		rfh = logging.handlers.RotatingFileHandler(
			filename=logfile,
			maxBytes=rotate_log_size, 
			backupCount=f.getconf("backup_log_count")
		)
		rfh.setFormatter(formatter)
		
		self.log = logging.getLogger(__name__)
		id_ = id(logger)
		self.log.setLevel(eval("logging."+loglevel))
		self.log.addHandler(rfh)
		self.log.info("return logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
	
	def getLogger(self):
		return self.log
	"""
	

	def __init__(self):
		pass
	
	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		from file_manager import File_manager as f
		f.getconf("loglevel", conffile=conffile)
		if(logfile==""):
			logfile = f.getconf("logdir", conffile=conffile) + f.getconf("logfile", conffile=conffile)
		loglevel = f.getconf("loglevel", conffile=conffile)
		rotate_log_size = f.getconf("rotate_log_size")

		import logging, logging.handlers
		logger = logging.getLogger()
		
		if len(logger.handlers) < 1:
			#fh = logging.FileHandler(filename="../../var/log/log2")
			#logger.addHandler(fh)
			rfh = logging.handlers.RotatingFileHandler(
				filename=logfile,
				maxBytes=rotate_log_size, 
				backupCount=f.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			logger.addHandler(rfh)

		#logging.basicConfig(filename="../../var/log/log2")

		id_ = id(logger)
		logger.setLevel(eval("logging."+loglevel))
		logger.info("return logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
		return logger

















