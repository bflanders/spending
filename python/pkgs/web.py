class Element(object):
    def __init__(self, tag='div', text='', eid='', kv={}, kv_sep='\n', ch=[]):
        self.tag = tag
        self.text = text
        self.eid = eid
        self.kv = kv
        self.kv_sep = kv_sep
        self.ch = []
        for child in ch:
            if isinstance(child, Element):
                self.ch.append(child)
            else:
                self.ch.append(Element(**child))
        
    def html(self, level=0):
        node = []
        indent = ' '*4*level
        line = f'{indent}<{self.tag}'+ (f' id="{self.eid}"' if self.eid else '')
        def get_kv(k,v):
            if k=='eid':
                return f'id={v}'
            else:
                return f'{k}={v}'
        if self.kv:
            if self.kv_sep != '\n':
                line += self.kv_sep  + self.kv_sep.join([get_kv(k,v)
                    for k,v in self.kv.items()
                    if not (self.eid and k=='eid')
                 ])
            else:
                line += self.kv_sep +\
                    self.kv_sep.join([f' {indent}{k}="{v}"'
                     for k,v in self.kv.items()
                     if not (self.eid and k=='eid')
                ])
            
        line += f'> {self.text} '
        node.append(line)
        if self.ch:
            for ch in self.ch:
                node.append(ch.html(level+1))
        if not (self.tag =='link' or self.tag =='meta'):
            node.append(f'{indent}</{self.tag}>')
        return '\n'.join(node)



class HTML(Element):
    def __init__(self, **kwargs):
        opts = {
            'tag': 'html'
            ,'kv': {
                'lang':'en'        
            }
            ,'kv_sep' : ' '
            ,'ch' : kwargs['ch'] if 'ch' in kwargs else []
        }
        Element.__init__(self, **opts)

class Head(Element):
    """
    <head>
    	<meta charset="utf-8">
        <title> Title </title> 
    """
    def __init__(self, *, title, ch=[]):
        opts = {
            'tag':'head'
            ,'ch':[
                 {'tag':'meta', 'kv':{ 'charset':'utf-8'}, 'kv_sep':' '}
                ,{'tag':'title', 'text':title }
            ]+ch
        }
        Element.__init__(self, **opts)        
 
class CSS(Element):
    def __init__(self,*,href,**kwargs):
        # Ignore kwargs except href; hacky?
        opts = {
            'tag':'link'
            ,'kv': {
                'rel':'stylesheet'
                ,'type':'text/css'
                ,'href':href
            }
            ,'kv_sep':' '
        }
        Element.__init__(self, **opts)

class JS(Element):      
    def __init__(self,*,src,**kwargs):
        opts = {
            'tag':'script'
            ,'kv':{ 
                'type':'text/javacript'
                ,'src':src
            }
            ,'kv_sep':' '
        }
        Element.__init__(self,**opts)
        
class Body(Element):
    def __init__(self,**kwargs):
        kwargs['tag'] = 'body'
        Element.__init__(self, **kwargs)
        
class Div(Element):
    def __init__(self, **kwargs):
        kwargs['tag'] = 'div'
        Element.__init__(self, **kwargs)        

class Span(Element):
    def __init__(self, **kwargs):
        kwargs['tag'] = 'span'
        Element.__init__(self, **kwargs)
        
class Form(Element):
    def __init__(self, **kwargs):
        kwargs['tag'] = 'form'
        Element.__init__(self, **kwargs)
        
class Button(Element):
    """
    <button id="table_cancel_btn" 
    	type="button" 
        class="btn btn-default" or "btn btn-primary"
        data-dismiss="modal">Cancel</button>
    """
    def __init__(self, *, label, **kwargs):
        kwargs['tag']='button'
        kwargs['text']=label
        if 'kv' in kwargs:
            kwargs['kv']['type']='button'
        else:
            kwargs['kv'] = {'type': 'button'}
        Element.__init__(self, **kwargs)
        
class DTable(Element):
    """
    <table id="c2tg_table" 
        class="table table-striped table-bordered dt-responsive" 
        style="width:100%">
    </table>
    """
    def __init__(self, *, eid, **kwargs):
        def_class = 'table table-striped table-bordered dt-responsive'
        kwargs['tag']='table'
        kwargs['eid']= eid
        kwargs['class'] = def_class in 'class' not in kwargs
            
        Element.__init__(self, **kwargs)
#%% Simple testing
if __name__=='__main__':
    d = Div(eid='div_id',kv={'attr':'value','eid':'bad_id'}, text='ok'
        ,ch=[Div(eid='child_id', kv={'attr':'level2'})])
    print(d.html())
    print(CSS(href="/path/to/file.css").html())
    h = Head(title='Title',ch=[
        CSS(href="/path/to/file.css")
    ])
    print(h.html())
