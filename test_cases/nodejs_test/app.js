/* 1. expressモジュールをロードし、インスタンス化してappに代入。*/
var sys = require('sys');
var express = require("express");
var app = express();

app.get('/', function (req, res) {
	//res.render('index', {});
	res.send('Hello Nodejs!');
});

/* 2. listen()メソッドを実行して3000番ポートで待ち受け。*/
var server = app.listen(3000, function(){
    console.log("Node.js is listening to PORT:" + server.address().port);
});

//app.get('/', function (req, res) {
//  res.render('index', {});
//});

/* 3. 以後、アプリケーション固有の処理 */
var log = require("./utils/log.js").getLogger();
log.debug("app.js start");
sys.log('Server running at http://localhost:3000/');



module.exports = app;
