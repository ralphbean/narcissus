function make_connection(a, b) {
        console.log("Dummy placeholder -- " + a + " " + b);
}

$(document).ready(function() {
        var counter = 0; 
        var lifetime = 3000;
        var base_radius = 1;
        var base_strength = 1;
        var bonus = 1;

        var w = 960
        var h = 700;

        // Setup a 'center width' and 'center height'
        var cw = w/2;
        var ch = h/2;

        var fill = d3.scale.category20();
        var nodes = [];
        var links = [];

        var vis = d3.select("#container").append("svg:svg")
        .attr("width", w)
        .attr("height", h);

        vis.append("svg:rect")
        .attr("width", w)
        .attr("height", h);

        var force = d3.layout.force()
        .charge(-130)
        .linkStrength(0.001)
        .linkDistance(1000)
        .nodes(nodes)
        .links(links)
        .size([w, h]);

        force.on("tick", function() {
                vis.selectAll("line.link")
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

                vis.selectAll("circle.node")
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });

        function denigrate_link(link) {
                link.source.r -= bonus;
                link.target.r -= bonus;
                link.strength -= bonus;

                if ( link.strength == base_strength ) {
                        for ( var i=0; i < links.length; i++ ) {
                                if ( links[i] == link ) {
                                        links.splice(i, 1);
                                        break;
                                }
                        }
                }

                if ( link.source.r == base_radius ) {
                        remove_node(link.source);
                }
                if ( link.target.r == base_radius ) {
                        remove_node(link.target);
                }
        }


        function remove_node(node) {
                for ( var i=0; i < nodes.length; i++ ) {
                        if ( nodes[i] == node ) {
                                nodes.splice(i, 1);
                                return true;
                        }
                }
                for ( var i=0; i < nodes.length; i++ ) {
                        if ( nodes[i] == node ) {
                                nodes.splice(i, 1);
                                return true;
                        }
                }

                restart();
                return false;
        }

        function find_link_by_nodes(a, b) {
                for ( var i = 0; i < links.length; i++ ) {
                        if ( (links[i].source == a && links[i].target == b) ||
                        (links[i].source == b && links[i].target == a)) {
                                return links[i];
                        }
                }
                return null;
        }

        function find_node_by_id(id) {
                for ( var i = 0; i < nodes.length; i++ ) {
                        if ( nodes[i].id == id ) {
                                return nodes[i];
                        }
                }
                return null;
        }

        function make_link(a, b) {
                if ( a == b ) { return; }
                link = {source: a, target: b, strength: base_strength};
                links.push(link);
                return link;
        }

        function make_connection(country, distro) {
                // Find the country and distro nodes.  If DNE, then create them.
                var c_node = find_node_by_id(country);
                var d_node = find_node_by_id(distro);
                if ( c_node == null ) {
                        c_node = make_node("country", country);
                }
                if ( d_node == null ) {
                        d_node = make_node("distro", distro);
                }

                // Search for a link between these two.
                var link = find_link_by_nodes(c_node, d_node);
                if ( link == null ) {
                        link = make_link(c_node, d_node);
                }
                link.strength += bonus;
                c_node.r += bonus;
                d_node.r += bonus;

                setTimeout( function(){denigrate_link(link);}, lifetime );

                restart();
        }
        window.make_connection = make_connection; // Expose!

        function make_node(cls, id) {
                var x = cw;
                var y = ch;
                var node = {
                        x: x,
                        y: y,
                        r: base_radius,
                        id: id,
                        cls: cls,
                        ttl: lifetime,
                };
                nodes.push(node);
                return node;
        }

        function restart() {
                var p;

                // Handle the links
                p = vis.selectAll("line.link")
                .data(links,
                        function(d) { return d.source.id + "_" + d.target.id }
                );

                p.style("stroke-width",
                        function(d) { return d.strength; }
                );

                p.enter().insert("svg:line", "circle.node")
                .attr("class", "link")
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

                p.exit().remove();


                // Handle the nodes
                p = vis.selectAll("circle.node")
                .data(nodes, function(d) { return d.id });

                p.attr("r", function(d) { return d.r; })

                p.enter().insert("svg:circle", "circle.cursor")
                .attr("class", function(d) { return "node " + d.cls; })
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; })
                .on("mouseover", function(d) {d.r += 5*bonus;})
                .on("mouseout", function(d) {d.r -= 5*bonus;})
                .call(force.drag);

                p.append("svg:title")
                .text(function(d) { return d.id });

                p.exit().remove();

                // This is expensive, if we can avoid it doing it so much.
                force.start();
        }
});
