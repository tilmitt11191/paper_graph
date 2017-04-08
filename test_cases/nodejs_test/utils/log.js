
var getconf = require("./getconf.js");

exports.getLogger = function() {
	console.log("logjs.getLogger start");
	var loglevel = getconf.getconf("loglevel");
	var log = require("log4js").getLogger();
	return log;
}


