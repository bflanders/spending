function Component(in_opts){
    var defaults = {
	    'tag': 'div'
	    ,'id':'' // element id shortcut
	    ,'cls': '' // class shortcut
	    ,'kv': {} // attributes
	    ,'_': '' // text
	    ,'par': document.body // Component parent
	    ,'app': 0 // app reference 
    }
    var self = this;
    var opts = Object.assign(defaults, in_opts);
    self.node = document.createElement(opts.tag);
    self.node.textContent = opts._
    // You must append child before you change attributes
    opts.par.appendChild(self.node);
    if (opts.cls){
        var clss = opts.cls.split(' ');
        for (var i=0; i<clss.length; i++){
            self.node.classList.add(clss[i]);
        }
    }
    if (opts.id){
	    self.node.id = opts.id;
    }
    // Set attributes
    if (opts.kv){
	    for (var prop in opts.kv){
	        if (opts.kv.hasOwnProperty(prop)){
		        if (!(
		            (prop === 'class' && opts.cls)
		            || (prop === 'id' && opts.id)
	    	    )){
		            var val = opts.kv[prop];
		            self.node.setAttribute(prop, val);
		        }
	        }
	    }
    }
    self.opts = opts;
    self.ch = [];
    self.reactions = {};
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
    return self;
}

Component.prototype.add_child = function(opts){
    var self = this;
    var char;
    if (opts instanceof Component){
        var ch = opts;
        ch.opts.par = self.node;
        ch.opts.app = self.opts.app;
    } else {
        var ch_opts = Object.assign(opts, {
            par: self.node
            ,app:self.opts.app
        });
        ch = new Component(ch_opts);
    }
    self.node.appendChild(ch.node);
    self.ch.push(ch);
}

Component.prototype.set_app = function(app){
    var self = this;
    self.opts.app = app;
    for (var i=0;i<self.ch.length;i++){
        self.ch[i].set_app(app);
    }
    return self;
}

Component.prototype.notifications = function(event_handlers){
    // event_handlers = { event: function }
    var self = this;
    var handler = 0;
    for (var e in event_handlers){
        if (event_handlers.hasOwnProperty(e)){
            handler = event_handlers[e].bind(self);
            self.node.addEventListener(e, handler); 
        }
    }
    return self; // chaining
}

Component.prototype.interests = function(reactions){
    // reactions = { topic: function }
    var self = this;
    var reaction = 0;
    for (var topic in reactions){
        if (reactions.hasOwnProperty(topic)){
            reaction = reactions[topic].bind(self);
            self.opts.app.register(topic, self);
            self.reactions[topic] = reaction;
        }
    }
    return self; // chaining
}

Component.prototype.react = function(topic, data) {
    var self = this;
    if (self.reactions.hasOwnProperty(topic)){
        self.reactions[topic](data);           
    }
}

Component.prototype.tell = function(topic, data){
    var self = this;
    var msg = {};
    msg[topic] = data;
    self.opts.app.bus.push(msg);
    self.opts.app.notify();
}
/* Do we need these? Should keep this "pure" and defer compositions
 * to main.js
 * 
function Div(opts){
    var div = opts || {};
    div.tag = 'div';
    Component.call(this, div);
}
Div.prototype = Object.create(Component.prototype);

function Span(opts){
    var span_opts = opts || {};
    span_opts.tag = 'span';
    Component.call(this, span_opts);
}
Span.prototype = Object.create(Component.prototype);
*/


