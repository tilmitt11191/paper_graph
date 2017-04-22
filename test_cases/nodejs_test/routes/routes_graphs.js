

var router = require('express').Router();
var cytoscape = require('cytoscape');
var mysql = require('mysql');
var log = require('..//utils/utils').getLogger();

function returnSuccess(res, data) {
  res.send({
    status: "success",
    data: data
  });
}

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'alladmin',
  password : 'admin',
  database : 'paper_graph'
});

router.get('/test', function(req, res, next){
		log.debug("routes_graphs.js router.post('/test', function(){ start")
		log.debug("aaa")
		returnSuccess(res, getGraphFromDB())
	}

)

function getGraphFromDB() {
	log.debug("getGraphFromDB start");
	var graph = {
		elements:[{data: { id: 'x' }}]
	}
	convertFromMySQLRecordsToCytoscape(graph);
	//convertNodesFromRecordsToCytoscape(nodes, cy);
	return graph;
}

function convertFromMySQLRecordsToCytoscape(graph) {
	log.debug("convertFromMySQLRecordsToCytoscape(graph) start");	
	log.debug("graph in starting method: " + graph)
	//connection.query('SELECT * from papers;', function (err, rows, fields, graph) {
	connection.query('SELECT * from papers;', function (err, results) {});
	log.debug("results: " + results)
/*		log.debug("graph in starting of connection: " + graph)
		if (err) { console.log('err: ' + err); }
		log.debug("rows.length: " + rows.length);
		log.debug("rows[0].id: " + rows[0].id);
		log.debug("rows[0].title: " + rows[0].title);
		log.debug("rows[1].id: " + rows[1].id);
		log.debug("rows[1].title: " + rows[1].title);
		log.debug("graph before forEach: " + graph)
		rows.forEach( function(row, graph) {
			node = '{"id": ' + row.id + '}';
			data = '{"data":' + node + '}';
			//graph.elements.push({data: node});
			graph["elements"] = JSON.parse(data);
		});
		log.debug("graph in connection: " + graph)
	});*/
	log.debug("graph out of connection: " + graph)
	connection.query('SELECT * from edges;', function (err, rows, fields, graph) {
		if (err) { console.log('err: ' + err); }
		rows.forEach( function(row, graph) {
			edge = {id: row.id, source: row.start, target: row.end};
			//graph.elements.push({data: edge});
		});
	});
}

function convertNodesFromRecordsToCytoscape(nodes) {
	for(node in nodes){
		log.debug(node);
	}
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
    name: 'breadthfirst',
    //name: 'cose',
    rows: 1
  }
}


module.exports = router;