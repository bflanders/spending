var app = (function(my){
    // Assemble components and set up messaging capability (bus + notifcation).
    my.bus = [] // [ { topic: data } ]
    my.listeners = {} // topic -> [ components ]
    my.register = function(topic, comp){
        if (my.listeners.hasOwnProperty(topic)){
            if (my.listeners[topic].indexOf(comp) == -1){
                my.listeners[topic].push(comp);
            }
        } else {
            my.listeners[topic] = [comp];
        }
    }

    // Notify all listeners
    my.notify = function(){
	    var msg;
	    while (msg = my.bus.pop()){
	        for (var topic in msg){
		        if (msg.hasOwnProperty(topic) && my.listeners.hasOwnProperty(topic)){
                    console.log('topic: "'+topic+'".');
                    var data = msg[topic];
		            my.listeners[topic].forEach(function(comp,i){
			            comp.react(topic, data);
		            });
		        }
	        }
	    }
    }
    
    // Compositions
    my.init = function(){
        var debug = function(data) { console.log(data); }
        var root = Div({cls:'wrapper'})
        var branding = {_:'Databasing', icon:'bullseye'};
        var li_items = [
            {_:'Setting',icon:'cog'}
            ,{_:'Refresh',icon:'sync'}
            ,{_:'Add',icon:'plus-circle'}
        ];
        root
            .add([sidenav(li_items,branding), content()])
            .set_app(my);
    }

    function content(){
        // Button to toggle sidenav
        side_btn = Tag({
            app:my
            ,tag:'button'
            ,kv:{
                'class':'btn btn-info'
                ,'id':'sb_collapse'
                ,'type':'button'
            }
        });
        side_btn.add([I('align-left'), Span({_:'Sidebar'})]);
        // Hacky in that it handles the click in a traditional way
        side_btn.notifications({'click': function(e){
            e.stopPropagation();
            this.tell('hide sidebar');
            // $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        }});

        var nav_cls = 'navbar navbar-expand-lg navbar-light bg-light';
        main_nav = Tag({tag:'nav',cls:nav_cls});
        main_nav.add(Div({cls:'container-fluid'}).add(side_btn));
        return Div({id:'content'})
            .add(main_nav)
            .interests({
                'hide sidebar': function(){
                    $(this.node).toggleClass('active');
                }
            });
    }
    
    function Tag(tag_opts){
        var opts = Object.assign(tag_opts,{app:my});
        return new Component(opts);
    }

    function I(icon,i_opts){
        var defaults = {tag:'i',cls:'fa fa-'+icon+' fa-fw'};
        var opts = Object.assign(i_opts||{}, defaults);
        return Tag(opts);
    }
    
    function Div(div_opts){
        var opts = Object.assign(div_opts,{tag:'div'});
        return Tag(opts);
    }

    function Span(span_opts){
        var opts = Object.assign(span_opts,{tag:'span'});
        return Tag(opts);
    }

    function A(opts, span_text, icon, brand){
        var a = opts || {};
        a.tag = 'a';
        brand ? a.cls='navbar-brand' : a.cls='nav-link pl-0';
        a.kv ? a.kv.href='#' : a.kv={href:'#'};
        var a = Tag(a);
        var i = 0, span = 0;
        if (icon){
            i = I(icon);
        }
        if (span_text){
            var span_cls = brand ? 'font-weight-bold' : 'd-md-inline';
            span = Span({'_':span_text, cls:span_cls});
        }
        i ? a.add(i) : null
        span ? a.add(span) : null
        return a;
    }

    function LI(li_opts,a){
        // LI(
        //   {par:ul.node, cls:'nav-item'}  # li options
        //   ,{}                            # a options
        //   ,'Databasing'                  # span text
        //   ,'bullseye'                    # icon
        //   ,true)                         # brand? 
        var opts = Object.assign(
            li_opts
            ,{tag:'li',cls:'nav-item',app:my} // override
        );
        var li = Tag(opts);
        li.add(a);
        return li;
    }

    function sidenav(li_items, branding){
        var nav = Tag({
            app:my
            ,tag:'nav'
            ,id:'sidebar'
        });
        nav.interests({
            'hide sidebar': function(){
                $(this.node).toggleClass('active');
            }
        });
        // Add branding, then add UL
        var ul_opts = {
            par:nav.node
            ,tag:'ul'
            ,cls:'list-unstyled components'
        }
        var ul = Tag(ul_opts), item;
        for (var i=0;i<li_items.length;i++){
            //item =- { _: ..., icon: ... }
            item = li_items[i];
            ul.add(LI({},A({},item._, item.icon,false)));
        }
        if (branding){
            if (branding.hasOwnProperty('_')){
                nav.add(A({},branding._, branding.icon || '',true));
            }
        }
        nav.add(ul)
        return nav;   
    }
 
    return my;
})(app || {})
