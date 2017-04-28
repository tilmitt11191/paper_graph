
# -*- coding: utf-8 -*-

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
			rfh = logging.handlers.RotatingFileHandler(
				filename=logfile,
				maxBytes=rotate_log_size, 
				backupCount=Conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			logger.addHandler(rfh)
			
			stream_handler = logging.StreamHandler()
			stream_handler.setFormatter(formatter)
			stream_handler.setLevel(Conf.getconf("loglevel_to_stdout", conffile=conffile))
			logger.addHandler(stream_handler)

		id_ = id(logger)
		logger.setLevel(eval("logging."+loglevel))
		logger.debug("return logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
		return logger













