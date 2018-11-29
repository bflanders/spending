function Component(opts){
    var defaults = {
	 'type': 'div'
	,'id':'' // element id shortcut
	,'cls': '' // class shortcut
	,'@': {} // attributes
	,'_': '' // text
	,'>':[] // Component children
	,'<': document.body // Component parent
	,')': {} // listen { topic: action }
	,'(': {} // notify
	,'app': 0 // app reference 
    }
    var self = this;
    var opts = Object.assign(defaults, opts);
    self.par = 0;
    self.node = document.createElement(opts.type);
    self.node.textContent = opts._
    // You must append child before you change attributes
    opts['<'].appendChild(self.node);
    if (opts.cls){
	self.node.classList.add(opts['cls']);
    }
    if (opts.id){
	self.node.id = self.opts.id;
    }
    if (opts['@']){
	for (var prop in opts['@']){
	    if (opts['@'].hasOwnProperty(prop)){
		if (!(
		    (prop === 'class' && opts.cls)
		    || (prop === 'id' && opts.id)
		)){
		    var val = opts['@'][prop];
		    self.node.setAttribute(prop, val);
		}
	    }
	}
    }
    if (opts.hasOwnProperty(')')){
	for (var topic in opts[')']){
	    if (opts[')'].hasOwnProperty(topic)){
		app.register(topic, self);
	    }
	}
    }
    // Recursive step
    opts['>'].forEach(function(item,i){
	var ch_opts = Object.assign(item, {
	    '<': self.node
	    ,'app': opts.app
	});
	var ch = item instanceof Component ? item : new Component(ch_opts);
	// Reassign parent?
	ch.opts['<'] = self.node;
	ch.par = self;
	self.node.appendChild(ch.node);
    });
    self.opts = opts;
}

Component.prototype.add = function(opts){
    var self = this;
    var ch_opts = Object.assign(opts, {'<': self.node});
    self.children.push(new Component(ch_opts));
    
}

Component.prototype.receive = function(topic, data) {
    var self = this;
    if (self.opts.hasOwnProperty(')')){
	if (self.opts[')'].hasOwnProperty(topic)){
	    self.opts[')'][topic](data)
	}
    }

}

function Div(opts){
    var div_opts = opts || {};
    div_opts.type = 'div';
    Component.call(this, div_opts);
}
Div.prototype = Object.create(Component.prototype);

function Span(opts){
    var span_opts = opts || {};
    span_opts.type = 'span';
    Component.call(this, span_opts);
}
Span.prototype = Object.create(Component.prototype);


function A(opts){
    var a_opts = opts || {};
    span_opts.type = 'a';
    Component.call(this, a_opts);
}
A.prototype = Object.create(Component.prototype);

function NavLI(text){
    var li_text =  text || '';
    var opts = {
	'type':'li'
	,'cls':'nav-item'
	,'>':[{
	    'type':'a'
	    , '@': { 'class':'nav-link','href':'#' }
	    ,'_':text
	}]
    }
    Component.call(this,opts);
}
NavLI.prototype = Object.create(Component.prototype);

function NavUL(cls, ch){
    var opts = {
	'type':'ul'
	,'cls':cls
	,'>': ch || []
    }
    Component.call(this,opts);
}
NavUL.prototype = Object.create(Component.prototype);
