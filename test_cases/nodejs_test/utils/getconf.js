
var sys = require('sys');
fs = require("fs")

function getconf(conf, conffile="../../etc/config.yml"){
	fs.statSync(conffile);
	var level = "loglevel";
	sys.log("loglevel[" + level + "]");
}