var app = (function (my) {
    my.roots = [];
    my.DEBUG = true;
    my.add_root = function (opts){
	// Ensure parent is document.body - intercept
	var defaults = {
	    '<': document.body
	    ,'app': my
	};
	root_opts = Object.assign(defaults, opts)
	my.roots.push(new Component(root_opts));
    }
    my.init = function(){
	if (my.DEBUG){
	    my.add_root({
		'type': 'div'
		,')': {
		    'debug': function(data){
			console.log(data);
		    }
		}
	    });
	}
    }
    return my;
})(app || {});
