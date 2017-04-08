
var getconf = require("getconf.js");

exports.getconf = function(conf, conffile="../../etc/config.yml"){
	fs.statSync(conffile);
	consol.log("this is getconf" + conf);
}