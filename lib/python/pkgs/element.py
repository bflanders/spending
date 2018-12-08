class Base(object):
    def __init__(self, *args, **kwargs): pass


class Element(Base):
    def __init__(self, **kwargs):
        opts = {
            'tag':'div'
            ,'text':''
            ,'eid':''
            ,'cls':''
            ,'kv':{}
            ,'kv_sep':'\n'
        }
        opts.update(kwargs)
        self.tag = opts['tag']
        self.text = opts['text']
        self.eid = opts['eid']
        self.cls = opts['cls']
        self.kv = opts['kv']
        self.kv_sep = opts['kv_sep']
        assertion_error = f"""
            Only space (' ') or newline ('\\n') allowed. 
            You gave {repr(self.kv_sep)}"""
        assert self.kv_sep==' ' or self.kv_sep=='\n', assertion_error
        self.ch = []    
    
    def add_child(self,child):
        if isinstance(child, Element):
            self.ch.append(child)
        else:
            self.ch.append(Element(**child))
    
    def add(self, children):
        if isinstance(children, list):
            for child in children:
                 self.ch.append(child)
        else:
             self.ch.append(children)
        return self
    
    def html(self, level=0):
        if self.eid:
            self.kv.update({'id':self.eid})
        if self.cls:
            self.kv.update({'class':self.cls})
        self.node = []
        indent = ' '*4*level
        line = f'{indent}<{self.tag}'
        kv_indent = '' if self.kv_sep != '\n' else (indent+'  ')
        if self.kv: 
            line += self.kv_sep
            line += self.kv_sep.join([f'{kv_indent}{k}="{v}"'
                for k,v in self.kv.items()
            ])
        
        line += f'> {self.text} '
        self.node.append(line)
        if self.ch:
            for ch in self.ch:
                self.node.append(ch.html(level+1))
        if not (self.tag =='link' or self.tag =='meta'):
            self.node.append(f'{indent}</{self.tag}>')
        return '\n'.join(self.node)

class HTML(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'html'
        self.kv.update({'lang':'en'})
        self.kv_sep = ' '
        
class Head(Element):
    """
    <head>
    	<meta charset="utf-8">
        <title> Title </title> 
    """
    def __init__(self, title):
        super().__init__()  
        self.tag = 'head'
        meta_charset = Element(tag='meta', kv={'charset':'utf-8'}, kv_sep=' ')
        meta_view = Element(tag='meta',kv={
            'name':'viewport'
            ,'content':"width=device-width, initial-scale=1.0"
        }, kv_sep=' ')
        meta_equiv = Element(tag='meta',kv={
            'http-equiv':"X-UA-Compatible" 
            ,'content': "IE=edge"
        },kv_sep=' ')
        ch_title = Element(tag='title',text=title )
        self.add([
            meta_charset
            ,meta_view
            ,meta_equiv
            ,ch_title
        ])
        # print('Object: '+str(self.__dict__).replace(',',',\n'))

class CSS(Element):
    def __init__(self,*,href,**kwargs):
        super().__init__(**kwargs)
        # Modify
        self.tag = 'link'
        self.kv.update({
            'rel':'stylesheet'
            ,'type':'text/css'
            ,'href':href
        })
        self.kv_sep = ' '
        # print('Object: '+str(self.__dict__).replace(',',',\n'))


class JS(Element):      
    def __init__(self,*,src,**kwargs):
        super().__init__(**kwargs)
        self.tag = 'script'
        self.kv.update({
            'type':'text/javascript'
            ,'src':src
        })
        self.kv_sep = ' '        

class Code(Element):      
    def __init__(self,*,src,**kwargs):
        super().__init__(**kwargs)
        self.tag = 'script'
        self.kv.update({
            'type':'text/javascript'
        })
        self.text = src
        self.kv_sep = ' '
        
class Body(Element):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.tag = 'body'

class Div(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.tag = 'div'

class Nav(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.tag = 'nav'

class Span(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'span'

class Form(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'form'

class A(Element):
    def __init__(self, href, **kwargs):
        super().__init__(**kwargs)
        if not self.kv:
            self.kv = {}
        self.kv['href']= href
        self.tag = 'a'

class I(Element):
    def __init__(self, *, icon, **kwargs):
        # opts = {'tag':'i', 'cls':f'fa fa-{icon} fa-fw','kv_sep':' '}
        super().__init__(**kwargs)
        self.tag = 'i'
        self.cls = f'fa fa-{icon} fa-fw'

class Button(Element):
    """
    <button id="table_cancel_btn" 
    	type="button" 
        class="btn btn-default" or "btn btn-primary"
        data-dismiss="modal">Cancel</button>
    """
    def __init__(self, *, label, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'button'
        self.text = label
        if not self.kv:
            self.kv = {}
        self.kv.update({'type': 'button'})

class Hamburger(Element):
    def __init__(self, *, target='navbar1', **kwargs):
        super().__init__(**kwargs)
        self.tag = 'button'
        self.cls = 'navbar-toggler navbar-toggler-right'
        if not self.kv:
            self.kv = {}
        self.kv.update({
            'type': 'button'
            ,'data-toggle':"collapse" 
            ,'data-target':f"#{target}"
        })
        self.add(Span(cls='navbar-toggler-icon',kv_sep=' '))
        
class DTable(Element):
    """
    <table id="c2tg_table" 
        class="table table-striped table-bordered dt-responsive" 
        style="width:100%">
    </table>
    """
    def __init__(self, *, eid, **kwargs):
        t_class = 'table table-striped table-bordered dt-responsive'
        super().__init__(**kwargs)
        self.tag = 'table'
        self.eid = eid
        self.cls = t_class

#%% Simple testing
if __name__=='__main__':
    d = Div(
        eid='div_id'
        ,kv={'attr':'value','id':'bad_id'}
        ,text='ok'
        ,cls='div_par_cls').add([
            Div(
                eid='child_id'
                ,cls='div_ch_cls'
                ,kv={'attr':'level2'})
            ,CSS(href="/path/to/file.css")
        ])
    print(d.html())
    """
    <div
      attr="value"
      eid="bad_id"
      id="div_id"> ok 
        <div
          attr="level2"
          id="child_id"
          class="div_cls">  
        </div>
        <link rel="stylesheet" type="text/css" href="/path/to/file.css">  
    </div>
    """
    h = Head(title='Title').add([
        CSS(href="/path/to/file.css")
    ])
    print(h.html())
    """
    <head>  
        <meta charset="utf-8">  
        <title> Title 
        </title>
        <link rel="stylesheet" type="text/css" href="/path/to/file.css">  
    </head>
    """
    a_cls='nav-link pl-0'
    span_cls='class="d-none d-md-inline"'
    icon = 'heart'
    label= 'Favorites'
    a=A(href='#', cls=a_cls, kv_sep=' ').add([
      I(icon=icon, kv_sep=' ')
      ,Span(cls=span_cls, text=label, kv_sep = ' ')
    ])
    print(a.html())
