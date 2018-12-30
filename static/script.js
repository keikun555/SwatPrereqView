$(document).ready(function() {
  $.when(loadData().done(function(graph_data) {
		var depts = graph_data[0];
		var allNodes = graph_data[1];
		var allEdges = graph_data[2];
		var container = document.getElementById('graph');
		var options = {
			layout: {
				hierarchical: {
					sortMethod: 'hubsize',
				}
			},
			physics: {
				barnesHut: {
					springConstant: 0,
					avoidOverlap: 0.2
				},
	      hierarchicalRepulsion: {
					nodeDistance: 190
				}
			}
		};
    
		setupSearch(depts, $('#term'), container, options, allNodes, allEdges);
  }));
	$('#graph').css({
		'width':    '100%',
		'height':   '100%',
		'position': 'absolute',
		'top':      '0', 
		'right':    '0', 
		'bottom':   '0', 
		'left':     '0',
		'z-index':  '0'
	});
})

function setupSearch(content, termTextElem, container, options, allNodes, allEdges) {
	// console.log(content.map(dept => ({title: dept})));
	var node_terms = allNodes.map(node => ({
		title: node['label'],
		description: node['dept'] + ' department',
		type: 'course'
	}));
	var dept_terms = content.map(dept => ({
		title: dept,
		description: 'Department',
		type: 'dept'	
	}));
	var random_term_group = [node_terms, dept_terms][Math.floor((Math.random() * 2))];
	var random_term = random_term_group[Math.floor((Math.random() * random_term_group.length))];
	update_network(random_term, termTextElem, container, options, allNodes, allEdges);
  $('#search').search({
		source: dept_terms.concat(node_terms),
		searchFields: ['title'],
	  onSelect: function(term, response) {
			update_network(term, termTextElem, container, options, allNodes, allEdges);
		  return true;
	  }
	})
}

function update_network(term, termTextElem, container, options, allNodes, allEdges) {
	var nodes = null;
	var edges = null;
	var name = term['title'];
	if(term['type'] == 'dept') {
		nodes = allNodes.filter(node => (node['dept'] == name));
		edges = allEdges.filter(edge => (edge['depts'].indexOf(name) >= 0));
	} else if(term['type'] == 'course') {
	  nodes = allNodes.filter(node => (node['label'] == name));
		var node_ids = nodes.map(node => (node['id']));
		edges = allEdges.filter(edge => 
			(node_ids.indexOf(edge['to']) >= 0 || node_ids.indexOf(edge['from']) >= 0));
	} else {
		console.log('Unknown search type encountered', term['type']);
	}
	var node = null;
	var valid = false;
	var validEdge = function(edge) {
		valid = true;
		if(nodes.filter(node => (node['id'] == edge['from'])).length <= 0) {
			node = allNodes.filter(node => (node['id'] == edge['from']))[0];
			if(node) {
				nodes.push(node);
			} else {
				valid = false;
			}
		}
		if(nodes.filter(node => (node['id'] == edge['to'])).length <= 0) {
			node = allNodes.filter(node => (node['id'] == edge['to']))[0];
			if(node) {
				nodes.push(node);
			} else {
				valid = false;
			}
		}
		return valid;
	}
	edges = edges.filter(edge => (validEdge(edge)));
	var data = {
		nodes: new vis.DataSet(nodes),
		edges: new vis.DataSet(edges)
	}
	var network = new vis.Network(container, data, options);
	termTextElem.text(name);
	network.on('doubleClick', function(params) {
		if(params.nodes.length > 0) {
			var clicked_term = {
				title: data.nodes.get(params.nodes[0])['label'],
				type: 'course'
			}
			update_network(clicked_term, termTextElem, container, options, allNodes, allEdges);
		}
	})
}

function loadData() {
  return $.ajax({
    dataType: "json",
    url: "/graph"
  });
}
