
$(function(){
	var host = window.location.href;
	if (host.charAt(host.length-1) == '#')
	host = host.substr(0, host.length-1);
	else if (host.charAt(host.length-1) != '/')
	host = host + "/";

	console.log("Host: " + host);


	function loadGraph() {
		var url = host + "graphs/data";
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
			//elements: graph.data,
			//elements: {"data": {"id": 241}},
			//elements: JSON.stringify(graph,null,'\t'),
			//elements: graph.toString(),
			//elements: JSON.parse(graph),
			//elements: convertToStr(graph),
			/*elements: {
				nodes: [
					{
						"data": {id: 1}
					},
					{
						"data": {id: 2}
					}
				],
				edges: [
					{
						"data": {id: "12", source: 1, target: 2}
					}
				]
			},*/
			/*elements: [
				{
					group: "node",
					"data": {id: 1}
				},
				{
					"data": {id: 2}
				},
				{
					"data": {id: "12", source: 1, target: 2}
				}
			],*/
			style: [ // the stylesheet for the graph
				{
					selector: 'node',
					style: {
						'width': '0.01px',
						'height': '0.01px',
						"background-color" : "#e03434",
						//"background-color" : "rgb(255,255,0)",
						//'background-color': 'red',
						//'color': '#000'
						//"color" : "rgb(0,0,0)",
						//"border" :  "rgb(255,255,255)",
						//"background-color" : "rgb(100,100,100)",
						//'background-width' : "100%",
						//'background-height' : "100%",
						//'backgroud-fit': 'contain',
						//"text-valign" : "center",
						//"text-halign" : "center"
					},
					selector: 'edge',
					style: {
						"width": "1px"
					},
					css: {
						'overlay-color': '#c0c0c0',
						'overlay-padding': '50px',
						'overlay-opacity': 100
					}
				},
				{
					"selector" : "node:selected",
					"css" : {
						//"background-color" : "rgb(255,255,0)",
						"background-color" : "rgb(255,0,255)",
						//"color": "rgb(0,0,0)"
					}
				}
			],
			zoom: 1,
			pan: { x: 0, y: 0 },
			minZoom: 1e-50,
			maxZoom: 1e50,
			zoomingEnabled: true,
			userZoomingEnabled: true,
			wheelSensitivity: 0.1
		})
	graph.forEach( function(data) {
		console.log("graph.length[" + graph.length + "], cy.add:" + data);
		//console.log("data.data:" + data.data);
		//cy.add(JSON.stringify(data,null,'\t'));
		cy.add( data );
		//cy.add(JSON.parse(data));
	});

	cy.boxSelectionEnabled(true)
	//cy.container()
	//cy.add(graph);
  //cy.add(JSON.stringify(graph,null,'\t'));
	var layout = cy.layout({
		//name: "null"
		//name: "preset"
		//name: "random"
		//name: 'grid'
		//name: "circle"
		//name: 'concentric'
		name: 'breadthfirst'
		//name: 'cose',
		//name: 'cose-bilkent'
 	});
	var cosebOptions = {
		name: 'cose-bilkent',
		// Called on `layoutready`
		ready: function () {
			console.log("layoutready")
		},
		// Called on `layoutstop`
		stop: function () {
			console.log("layoutstop")
		},
		// number of ticks per frame; higher is faster but more jerky
		refresh: 30,
		// Whether to fit the network view after when done
		fit: true,
		// Padding on fit
		padding: 10,
		// Padding for compounds
		paddingCompound: 15,
		// Whether to enable incremental mode
		//randomize: true,
		randomize: false,
		// Node repulsion (non overlapping) multiplier
		nodeRepulsion: 4500,
		//nodeRepulsion: 0,
		// Ideal edge (non nested) length
		idealEdgeLength: 50,
		// Divisor to compute edge forces
		edgeElasticity: 0.45,
		// Nesting factor (multiplier) to compute ideal edge length for nested edges
		nestingFactor: 0.1,
		// Gravity force (constant)
		gravity: 0.25,
		// Maximum number of iterations to perform
		numIter: 250000,
		// For enabling tiling
		//tile: true,
		tile: false,
		// Type of layout animation. The option set is {'during', 'end', false}
		//animate: 'end',
		//animate: 'during',
		animate: false,
		// Represents the amount of the vertical space to put between the zero degree members during the tiling operation(can also be a function)
		tilingPaddingVertical: 10,
		// Represents the amount of the horizontal space to put between the zero degree members during the tiling operation(can also be a function)
		tilingPaddingHorizontal: 10,
		// Gravity range (constant) for compounds
		gravityRangeCompound: 1.5,
		// Gravity force (constant) for compounds
		gravityCompound: 1.0,
		// Gravity range (constant)
		gravityRange: 3.8
	};


/*	var options = {
		name: 'cose',

		// Called on `layoutready`
		ready: function(){},

		// Called on `layoutstop`
		stop: function(){},

		// Whether to animate while running the layout
		animate: true,

		// The layout animates only after this many milliseconds
		// (prevents flashing on fast runs)
		animationThreshold: 250,

		// Number of iterations between consecutive screen positions update
		// (0 -> only updated on the end)
		//refresh: 20,
		refresh: 1,

		// Whether to fit the network view after when done
		//fit: true,
		fit: false,

		// Padding on fit
		//padding: 30,
		padding: 100,

		// Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
		boundingBox: undefined,

		// Randomize the initial positions of the nodes (true) or use existing positions (false)
		//randomize: false,
		randomize: true,

		// Extra spacing between components in non-compound graphs
		//componentSpacing: 100,
		componentSpacing: 0,

		// Node repulsion (non overlapping) multiplier
		//nodeRepulsion: function( node ){ return 400000; },
		nodeRepulsion: function( node ){ return 0; },

		// Node repulsion (overlapping) multiplier
		//nodeOverlap: 10,
		nodeOverlap: 1,

		// Ideal edge (non nested) length
		idealEdgeLength: function( edge ){ return 10; },

		// Divisor to compute edge forces
		//edgeElasticity: function( edge ){ return 100; },
		edgeElasticity: 20,

		// Nesting factor (multiplier) to compute ideal edge length for nested edges
		nestingFactor: 5,

		// Gravity force (constant)
		//gravity: 80,
		gravity: 0,

		// Maximum number of iterations to perform
		numIter: 1000,

		// Initial temperature (maximum node displacement)
		initialTemp: 200,

		// Cooling factor (how the temperature is reduced between consecutive iterations
		//coolingFactor: 0.95,
		coolingFactor: 0.1,

		// Lower temperature threshold (below this point the layout will end)
		minTemp: 1.0,

		// Pass a reference to weaver to use threads for calculations
		weaver: false
	};
	cy.layout(options);*/
	//cy.layout(cosebOptions);
	//cy.viewport({
		//zoom: 1,
		//pan: { x: 1, y: 1 }
	//});
	/*cy.animate({
		pan: { x: 100, y: 100 },
		zoom: 1
	}, {
		duration: 1000
	});*/
	console.log("layout.run() start")
	layout.run();
	console.log("showGraph finished");
	}


	loadGraph();
});

function convertToStr(graph){
	//return {node: {data: {id: 1}}, {data: {id: 2}}};
	//return {node: {data: {id: 1}}, {data: {id: 2}}};
	//return {node: {data: {id: 1}}};
}

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
