
var sys = require('sys');
var getconf = require("./getconf.js");

function getLogger() {
	alert("this is getLogger()");
	sys.log("logjs.getLogger start");
	var loglevel = getconf.getconf("loglevel");
	var log = require("log4js")
	log4js.configure({
	appenders: [
		{ type: 'file', filename: 'debug.log' }
  ]
});
	var logger = log.getLogger();
	logger.setLevel(loglevel);
}


