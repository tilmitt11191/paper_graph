
const yaml = require('js-yaml');
const fs = require('fs');

exports.getConf = function(target) {
	var confFile = "../../etc/config.yml"
	try {
		const confs = yaml.safeLoad(fs.readFileSync(confFile, 'utf8'));
		var targetConf = eval("confs." + target);
	  return targetConf;
	} catch (e) {
	  console.log(e);
	}
}

exports.getLogger = function () {
	var log4js = require("log4js");
	log4js.loadAppender('file');
	var logfile = this.getConf("logdir") + this.getConf("node_logfile");
	log4js.addAppender(log4js.appenders.file(logfile));
	var log = log4js.getLogger();
	log.debug("return logger. logfile[" + logfile + "]");
	return log;
}
