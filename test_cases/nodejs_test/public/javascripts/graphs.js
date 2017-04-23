
$(function(){
	var host = window.location.href;
	if (host.charAt(host.length-1) == '#')
	host = host.substr(0, host.length-1);
	else if (host.charAt(host.length-1) != '/')
	host = host + "/";

	console.log("Host: " + host);


	function loadGraph() {
		var url = host + "graphs/test";
		console.log("loadGraph url:" + url);
		$.get(url).done(function(response) {
			console.log("$ get done");
			//console.log("response.data[" + response.data + "]");
			showGraph(response.data);
		});
	}

	function showGraph(graph) {
		//console.log("showGraph(graph) graph:" + graph);
		var cy = cytoscape({
			container: document.getElementById('graph'), // container to render in
			//elements: graph,
			//elements: {node: {data: {id: 1}}},
			//elements: graph.data[0],
			//elements: {"data": {"id": 241}},
			//elements: JSON.stringify(graph,null,'\t'), 
			//elements: graph.toString(),
			//elements: JSON.parse(graph), 
			style: [ // the stylesheet for the graph
				{
					selector: 'node',
					style: {
						'background-color': '#fff',
						'label': 'data(id)',
						"color" : '#000',
						"text-valign" : "center",
						"text-halign" : "center"
					}
				},
				{
					selector: 'edge',
					style: {
					'width': 0.5,
					'line-color': '#ccc',
					'target-arrow-color': '#ccc',
					'target-arrow-shape': 'triangle'
					}
				},
				{
					"selector" : "node:selected",
					"css" : {
						"background-color" : "rgb(255,255,0)",
						"color": "rgb(0,0,0)"
					}
				}
			],
			// initial viewport state:
			zoom: 1,
			pan: { x: 0, y: 0 },
			// rendering options:
			wheelSensitivity: 0.5,
	})
	//cy.add(graph);
  //cy.add(JSON.stringify(graph,null,'\t'));
  graph.forEach( function(data) {
	  console.log("graph.length[" + graph.length + "], cy.add:" + data);
	  //console.log("data.data:" + data.data);
	  //cy.add(JSON.stringify(data,null,'\t'));
	  cy.add( data );
	  //cy.add(JSON.parse(data));
	});
	var layout = cy.layout({
		//name: "null"
		//name: "preset"
		//name: "random"
		//name: 'grid'
		//name: "circle"
		name: 'concentric'
		//name: 'breadthfirst'
 	});
	layout.run();
	/*
	cy.add( {"data": {"id": 11}} );
	cy.add( {"data": {"id": 22}} );
	cy.add( {"data": {"id": 10, "source": 11, "target": 22}} );
	*/
  console.log("showGraph finished");
	}

		
	loadGraph();
});
/*
var cy = cytoscape({
  
  container: document.getElementById('cy'), // container to render in
  elements: [ // list of graph elements to start with
    { // node a
      data: { id: 'a' }
    },
    { // node b
      data: { id: 'b' }
    },
    { // edge ab
      data: { id: 'ab', source: 'a', target: 'b' }
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
		name: "preset", 
    //name: 'grid',
    //rows: 2
    //name: 'random',
    //name: 'concentric',
    //name: 'breadthfirst',
    //name: 'cose',
  }
});
console.log("container[" + cy.container + "]");  
cy.nodes().forEach(function( ele ){
  console.log( ele.id() );
});
*/
var renewal = document.getElementById("renew");
console.log(renewal);

renewal.onclick = function(){
	console.log("renew!");
}
/*

renewal.onclick = renew2;
*/
/*
$(function(){
  //document.write("Hello World!!");
  connect_to_db();
});

function connect_to_db(){
	var $list = $('.list');
	$list.append('<p>aaa</p>');
	$list.fadeIn();
}
*/

/*
$(function(){

	var log = require("../utils/log.js").getLogger();
	log.info("graphs.js start");

	function alerttest(){
		log.info("alerttest start");
	
	};
});
*/

