class Element(object):
    def __init__(self, tag='div', text='', id='', kv={}, kv_sep='\n', ch=[]):
        self.tag = tag
        self.text = text
        self.id = id
        self.kv = kv
        self.kv_sep = kv_sep
        self.ch = ch
        
    def html(self, level=0):
        node = []
        indent = ' '*4*level
        line = f'{indent}<{self.tag}'+ (f' id="{self.id}"' if self.id else '')
        
        if self.kv:
            line += self.kv_sep +\
                self.kv_sep.join([f' {indent}{k}="{v}"'
                 for k,v in self.kv.items()
                 if not (self.id and k=='id')
            ])
            
        line += f'>{self.text}'
        node.append(line)
        if self.ch:
            for ch in self.ch:
                node.append(ch.html(level+1))
        if not (self.tag =='link' or self.tag =='meta'):
            node.append(f'{indent}</{self.tag}>')
        return '\n'.join(node)

class Div(Element):
    def __init__(self, **kwargs):
        kwargs['tag'] = 'div'
        Element.__init__(self, **kwargs)
        
class Span(Element):
    def __init__(self):
        kwargs['tag'] = 'span'
        Element.__init__(self, **kwargs)

class CSS(Element):
    def __init__(self,*,src,**kwargs):
        kwargs['tag']='link'
        kwargs['kv']={
            'rel':'stylesheet'
            ,'type':'text/css'
            ,'href':src
        }
        kwargs['kv_sep']=' '
        Element.__init__(self, **kwargs)
        
if __name__=='__main__':
    d = Div(id='divid',kv={'src':'text/css', 'attr':'value'}, text='ok'
        ,ch=[Div(id='chid', kv={'attr':'level2'})])
    print(d.html())
    print(CSS(src="src").html())
