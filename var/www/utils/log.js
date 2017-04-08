
var getconf = require("getconf.js");

exports.getLogger = function() {
	var loglevel = getconf("loglevel");
	var log = Logger.getLogger();
	return log;
}


