
var router = require('express').Router();
var async = require('async');
var cytoscape = require('cytoscape');
var mysql = require('mysql');
var log = require('../utils/utils').getLogger();

//var markovCluster = require('../lib/cytoscape.js-markov-cluster/cytoscape-markov-cluster.js');
//markovCluster( cytoscape ); // register extension
var regCose = require('cytoscape-cose-bilkent');
regCose( cytoscape ); // register extension

var startNode = 1;
var endNode = 15;
//var endNode = 1500000;
var relevancyThreshold = 4;

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'alladmin',
  password : 'admin',
  database : 'paper_graph'
});


function returnSuccess(res, data) {
	res.send({
		status: "success",
		data: data
	});
}

router.get('/data', function(req, res, next){
	test()
});
test()
async function test() {
	log.debug("routes_graphs.js router.post('/data', function(){ start");
	var graph = await [];
	var nodesDataString = await getPapersFromMysql(graph)
	//var edgesDataString = await ""
	var tmp = await createGraph(graph, nodesDataString, edgesDataString)
	log.debug("nodesDataString: " + nodesDataString)
}

function getPapersFromMysql(graph) {
	return p = new Promise((resolve, reject) => {
		log.debug('SELECT * from papers where ' + startNode + '  < id and id < ' + endNode + ';')
		connection.query('SELECT * from papers where ' + startNode + ' < id and id < ' + endNode + ';', function (err, rows, fields) {
			if (err) { console.log('err: ' + err); }
			log.debug("node num: " + rows.length);
			
			//rows.forEach( function(row) {
			rows.some( function(row) {
				log.debug("row.id: " + row.id);
				//node = '{"id": ' + row.id + ', "weight": ' + 1 + '}';
				//data = '{"data": ' + node  + '}';
				data = {
					"data": {
						"id": row.id
					}
				}
				//log.debug("graph.push(" + JSON.stringify(data,null,'\t') + ")")
				//graph.push(JSON.stringify(data,null,'\t'));
				graph.push(data);
				log.debug(graph.length + " > " + (endNode - startNode));
				if(graph.length > (endNode - startNode)){
					log.debug("if")
					return "aaa"
				}
				//graph.push(JSON.parse(data));
			});
			log.debug("graph.length after add nodes: " + graph.length);
		});
	});
}

/*
router.get('/data', function(req, res, next){
	log.debug("routes_graphs.js router.post('/test', function(){ start");
	var graph = [];
	var nodesDataString = ""
	var edgesDataString = ""
	async.waterfall([
		function(callback){
			getPapersFromMysql(callback, graph);
		},
		function(callback){
			getEdgesFromMysql(callback, graph);
		},*//*
		function(callback){
			createGraph(callback, graph);
		},*/
/*		function(callback){
			var clusters = graph.elements().markovCluster({
				expandFactor: 2,        // affects time of computation and cluster granularity to some extent: M * M
				inflateFactor: 2,       // affects cluster granularity (the greater the value, the more clusters): M(i,j) / E(j)
				multFactor: 1,          // optional self loops for each node. Use a neutral value to improve cluster computations.
				maxIterations: 10,      // maximum number of iterations of the MCL algorithm in a single run
				attributes: [           // attributes/features used to group nodes, ie. similarity values between nodes
    			function(edge) {
						return edge.data('weight');
					}
					// ... and so on
				]
			});
			callback(null);
		},*//*
		function(callback){
			log.debug("graph.length before return: " + graph.length);
			//graph.forEach( function(el){
				//log.debug("el: " + el);
			//});
			returnSuccess(res, graph);
			//returnSuccess(res, sampleGraph);
		}
	]);
});*/

/*
function getPapersFromMysql(callback, graph) {
	//connection.query('SELECT * from papers;', function (err, rows, fields) {
	log.debug('SELECT * from papers where ' + startNode + '  < id and id < ' + endNode + ';')
	connection.query('SELECT * from papers where ' + startNode + ' < id and id < ' + endNode + ';', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("node num: " + rows.length);
		
		//rows.forEach( function(row) {
		rows.some( function(row) {
			log.debug("row.id: " + row.id);
			//node = '{"id": ' + row.id + ', "weight": ' + 1 + '}';
			//data = '{"data": ' + node  + '}';
			data = {
				"data": {
					"id": row.id
				}
			}
			//log.debug("graph.push(" + JSON.stringify(data,null,'\t') + ")")
			//graph.push(JSON.stringify(data,null,'\t'));
			graph.push(data);
			log.debug(graph.length + " > " + (endNode - startNode));
			if(graph.length > (endNode - startNode)){
				log.debug("if")
				return true;
			}
			//graph.push(JSON.parse(data));
		});
	log.debug("graph.length after add nodes: " + graph.length);
	callback(null);
	});
}
*/
function getEdgesFromMysql(callback, graph) {
	log.debug("getEdgesFromMysql(graph) start");
	log.debug("graph.length: " + graph.length)
	/*
	query = 'SELECT * from edges;';
	records = mysql.format(query);
	log.debug("edge num: " + records.length);
	callback(null);
	*/
	/*
	var query = connection.query('SELECT * from edges;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
	});
	log.debug("edge num: " + query.length);
	*/
	log.debug('SELECT * from edges where ' + 
	startNode + '  < start and start < ' + endNode + ' and ' + 
	startNode + '  < end and end < ' + endNode +';')
	//connection.query('SELECT * from edges;', function (err, rows, fields) {
	connection.query('SELECT * from edges where ' + 
	startNode + '  < start and start < ' + endNode + ' and ' + 
	startNode + '  < end and end < ' + endNode +';', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("edge num: " + rows.length);
		log.debug("graph.length before add edges: " + graph.length);
		rows.forEach( function(row) {
			//if(row.relevancy < relevancyThreshold && startNode <= row.start && row.start < endNode && startNode < row.end && row.end < endNode ){
			if(row.relevancy >= relevancyThreshold){
				//edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
				//data = '{"data":' + edge + '}';
				log.debug("edge = {id: " + row.id + ", source: " + row.start + ", target: " + row.end + "};")
				data = {
					"data": {
						//"id": row.id,
						"source": row.start,
						"target": row.end
					},
					"style": {
						'width': row.relevancy/6,
						'line-color': '#ccc',
						'target-arrow-color': '#ccc',
						'target-arrow-shape': 'triangle'
					}
				}
				//graph.push(JSON.stringify(data,null,'\t'));
				graph.push(data);
			}
		});
		//log.debug("graph.length after add edges: " + graph.length);
		callback(null);	
	});	
}

function createGraph(graph, nodesDataString, edgesDataString){
	return new Promise((resolve, reject) => {
		log.debug("createGraph")
		log.debug("nodesDataString: " + nodesDataString)
	});
}

function convertFromMySQLRecordsToCytoscape(graph) {
	log.debug("convertFromMySQLRecordsToCytoscape() start");
	connection.query('SELECT * from papers;', function (err, rows, fields, graph) {
		if (err) { console.log('err: ' + err); }
		log.debug("node num: " + rows.length);
		/*
		rows.forEach( function(row) {
			node = {"id": row.id};
			data = {"data": node};
			//log.debug("graph.push(" + JSON.stringify(data,null,'\t') + ")")
			graph.push(data);
		});
		log.debug("graph.length after add nodes: " + graph.length);
		*/
	});
	
	connection.query('SELECT * from edges;', function (err, rows, fields) {
		if (err) { console.log('err: ' + err); }
		log.debug("edge num: " + rows.length);
		/*rows.forEach( function(row) {
			if(row.relevancyThreshold > 1){
				edge = '{"id": ' + row.id + ', "source": ' + row.start + ', "target": ' + row.end + '}';
				data = '{"data":' + edge + '}';
				graph.push(data);
			}
		});*/
		//log.debug("graph.length after add edges: " + graph.length);
	});

	log.debug("graph.length method finished: " + graph.length);
	return graph;
	//return sampleGraph;
}


var sampleGraph = {
 elements: [ // list of graph elements to start with
    { // node a
      data: { id: 'x' }
    },
    { // node b
      data: { id: 'y' }
    },
    { // edge ab
      data: { id: 'xy', source: 'x', target: 'y' }
    }
  ],

  style: [ // the stylesheet for the graph
    {
      selector: 'node',
      style: {
        'background-color': '#666',
        'label': 'data(id)'
      }
    },

    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle'
      }
    }
  ],

  layout: {
    //name: 'grid',
    //name: 'random',
    //name: 'concentric',
    //name: 'breadthfirst',
    //name: 'cose',
    //rows: 1
  }
}


module.exports = router;
