var app = (function (self) {
    var roots = [];
    var DEBUG = true;
    self.add_root = function (opts){
	// Ensure parent is document.body - intercept
	var defaults = {
	    '<': document.body
	    ,'app': self
	};
	root_opts = Object.assign(defaults, opts)
	self.roots.push(new Component(root_opts));
    }
    self.init = function(){
	if (DEBUG){
	    self.add_component({
		'type': 'div'
		,')': {
		    'debug': function(data){
			console.log(data);
		    }
		}
	    });
	}
    }
})(app || {});
