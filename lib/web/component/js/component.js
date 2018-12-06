function Component(in_opts){
    var defaults = {
	 'type': 'div'
	,'id':'' // element id shortcut
	,'cls': '' // class shortcut
	,'attr': {} // attributes
	,'_': '' // text
	,'par': document.body // Component parent
	,'app': 0 // app reference 
    }
    var self = this;
    var opts = Object.assign(defaults, in_opts);
    self.par = opts.par;
    self.node = document.createElement(opts.type);
    self.node.textContent = opts._
    // You must append child before you change attributes
    opts.par.appendChild(self.node);
    if (opts.cls){
	self.node.classList.add(opts['cls']);
    }
    if (opts.id){
	self.node.id = self.opts.id;
    }
    if (opts.attr){
	for (var prop in opts.attr){
	    if (opts.attr.hasOwnProperty(prop)){
		if (!(
		    (prop === 'class' && opts.cls)
		    || (prop === 'id' && opts.id)
		)){
		    var val = opts.attr[prop];
		    self.node.setAttribute(prop, val);
		}
	    }
	}
    }
    // Default fields. Modified by subsequent methods
    self.ch = []; // see .add( childs )
    self.react = {}; // topic -> [ callbacks ]; see .listen(topic, fn)
    self.opts = opts;
}

Component.prototype.add = function(childs){
    var self = this;
    if (childs instanceof Array){
	for (var i=0; i<childs.length; i++){
	    self.add_child(childs[i]);
	}
    } else {
	self.add_child(childs);
    }
}

Component.prototype.add_child = function(child){
    var self = this;
    if (child instanceof Component){
	child.app = self.app; // Necessary?
	self.opts.ch.push(child)
    } else {
	var ch_opts = Object.assign(opts, {
	    par: self.node
	    ,app: self.app
	});
	self.children.push(new Component(ch_opts));
    }
}

Component.prototype.listen = function(topic, reaction){
    var self = this;
    if (self.react.hasOwnProperty(topic)){
	self.react[topic].push(reaction.bind(self));
    } else {
	self.react[topic] = [reaction.bind(self)];
}

Component.prototype.receive = function(topic, data) {
    var self = this;
    if (self.react.hasOwnProperty(topic)){
	    self.react[topic](data)
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
    a_opts.type = 'a';
    a_opts.attr = { href:'#' };
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
