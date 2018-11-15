var app = (function (self) {
    var bus = {}; //m { topic: [ comps ]
    self.register = function(topic, component){
	if self.bus.hasOnwProperty(topic){
	    self.bus[topic].push(component);
	} else {
	    self.bus[topic] = [component];
	}
    }
    self.notify = function(topici, data){
	if (self.bus.hasOwnProperty(topic)){
	    while (var sub = self.bus.pop()){
		sub.receive(topic, data);
	    }
	}
    }
})(app || {});
