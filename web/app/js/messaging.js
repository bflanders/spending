var app = (function (my) {
    my.bus = {}; // { topic: [ comps ]
    my.register = function(topic, component){
	if (my.bus.hasOwnProperty(topic)){
	    my.bus[topic].push(component);
	} else {
	    my.bus[topic] = [component];
	}
    }
    my.notify = function(topic, data){
	if (my.bus.hasOwnProperty(topic)){
	    var comp;
	    for (var i=0; i < my.bus[topic].length; i++){
		comp = my.bus[topic][i];
		comp.receive(topic, data);
	    }
	}
    }
    return my;
})(app || {});
