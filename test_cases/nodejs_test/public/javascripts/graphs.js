
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
		var cy = cytoscape({
			container: document.getElementById('graph'), // container to render in
 			elements: graph.elements,
			style: graph.style,
			layout: graph.layout
		})
	}

/*
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
*/
		
	loadGraph();
});

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

