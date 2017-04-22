
var port = 3001;

var express = require('express');
var app = express();
var path = require('path');

var log = require('./utils/utils').getLogger();
log.debug("routes_graph.js start");

app.set('views', path.join(__dirname + '/views'));
app.set('view engine', 'pug');

app.use(express.static(path.join(__dirname, 'public')));
//app.use('/', express.static(__dirname + '/'));
//app.use(express.static(path.join(__dirname, 'public')));

var routes = require('./routes/index');
app.use('/', routes);
var graphs = require("./routes/routes_graphs")
app.use('/graphs', graphs);








app.listen(port,function(){
	log.info("Expressサーバーがポート%dで起動しました。モード:%s",port,app.settings.env)
	});


module.exports = app;
