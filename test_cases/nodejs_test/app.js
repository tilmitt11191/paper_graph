var express = require('express');
var app = express();

app.set('view engine', 'pug');
app.set('views', __dirname + '/views');

app.get('/', function (req, res) {
  res.render('index', { title: 'Express Sample' });
});
var port = 3000;
//app.listen(port);

// set static file dir
app.use('/', express.static(__dirname + '/'));

app.listen(port,function(){
	console.log("Expressサーバーがポート%dで起動しました。モード:%s",port,app.settings.env)
	});
