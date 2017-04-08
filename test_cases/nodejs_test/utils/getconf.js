
fs = require("fs")

exports.getconf = function (conf, conffile="../../etc/config.yml") {
	//fs.statSync(conffile);

	var level = "loglevel";
	console.log("loglevel[" + level + "]");
}