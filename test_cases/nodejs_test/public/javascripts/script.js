
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
    //name: 'grid',
    //name: 'random',
    //name: 'concentric',
    name: 'breadthfirst',
    //name: 'cose',
    rows: 1
  }
});
console.log("container[" + cy.container + "]");  
cy.nodes().forEach(function( ele ){
  console.log( ele.id() );
});
/*
// Code goes here
$(function(){
  $('#cy').cytoscape({
    style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'content': 'data(name)',
          'color': 'white',
          'text-outline-width': 2,
          'text-outline-color': '#888'
        })
      .selector('edge')
        .css({
          'target-arrow-shape': 'triangle'
        })
      .selector(':selected')
        .css({
          'background-color': 'black',
          'line-color': 'black',
          'target-arrow-color': 'black',
          'source-arrow-color': 'black'
        })
      .selector('.faded')
        .css({
          'opacity': 0.25,
          'text-opacity': 0
        }),
    
    elements: {
      nodes: [
        { data: { id: 'j', name: 'Jerry' } },
        { data: { id: 'e', name: 'Elaine' } },
        { data: { id: 'k', name: 'Kramer' } },
        { data: { id: 'g', name: 'George' } }
      ],
      edges: [
        { data: { source: 'j', target: 'e' } },
        { data: { source: 'j', target: 'k' } },
        { data: { source: 'j', target: 'g' } },
        { data: { source: 'e', target: 'j' } },
        { data: { source: 'e', target: 'k' } },
        { data: { source: 'k', target: 'j' } },
        { data: { source: 'k', target: 'e' } },
        { data: { source: 'k', target: 'g' } },
        { data: { source: 'g', target: 'j' } }
      ]
    },
    // layout: {
    //   name: 'random'
    // },
    ready: function(){
      window.cy = this;
      
      // giddy up...
      
      cy.elements().unselectify();
      
      cy.on('tap', 'node', function(e){
        var node = e.cyTarget; 
        var neighborhood = node.neighborhood().add(node);
        
        cy.elements().addClass('faded');
        neighborhood.removeClass('faded');
      });
      
      cy.on('tap', function(e){
        if( e.cyTarget === cy ){
          cy.elements().removeClass('faded');
        }
      });
      
      cy.layout({
        name: 'random'
      });
    }
  });
});
*/