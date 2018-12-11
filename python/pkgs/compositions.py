#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 14:09:37 2018

@author: ben
"""
from sys import path
path.append('/home/ben/projects/databasing/lib/python/pkgs')
from element import Element, Div, Nav, Span, I

class Item(Element):
    def __init__(self, *, label, icon, brand=False, **kwargs):
        super().__init__(**kwargs)
        if not self.kv:
            self.kv = {}
        self.kv['href']= '#'
        self.cls='navbar-brand' if brand else 'nav-link pl-0'
        span_cls='font-weight-bold' if brand else 'd-md-inline'
        self.tag = 'a'
        self.add([
              I(icon=icon, kv_sep=' ')
              ,Span(cls=span_cls, text=label, kv_sep = ' ')
            ])
    
class LI(Element):
    """
    <li class="nav-item">
        <a class="nav-link pl-0" href="#">
            <i class="fa fa-heart-o fa-fw">
            </i> 
            <span class="d-md-inline">Link
            </span>
        </a>
    </li>
    """
    def __init__(self, *, label, icon,**kwargs):
        super().__init__(**kwargs)
        self.tag = 'li'
        self.cls = 'nav-item'
        self.kv_sep = ' ' 
        self.add(Item(label=label, icon=icon, brand=False))


def sidenav(branding=('Brand','bullseye'), li_items=[]):
    assert len(li_items) > 0, "Must have nav list items"
    
    # Branding
    blabel, bicon = branding
    brand_item = Div(cls="sidebar-header").add(
        Item(label=blabel,icon=bicon, brand=True)
    )
    
    # UL
    ul = Element(tag='ul',cls="list-unstyled components")
    ul.add([LI(label=ti[0], icon=ti[1]) for i,ti in enumerate(li_items)])
    
    # Compose from nav down
    nav = Nav(eid='sidebar').add([
        brand_item
        ,ul
    ])
    return nav

def content():
    sidebar_btn = Element(tag='button',kv={
        'class': 'btn btn-info'
        ,'id': 'sidebarCollapse'
        ,'type': 'button'
    }).add([
        I(icon='align-left')
        ,Span(text='Sidebar')
    ])
    
    return Div(eid='content').add([
        Nav(cls='navbar navbar-expand-lg navbar-light bg-light').add(
            Div(cls='container-fluid').add(sidebar_btn)
        )
        ,Element(tag='h2',text='Table Title')            
    ])

def default_body(branding=('Brand','bullseye'),li_items=[]):
    sidebar = sidenav(branding, li_items=li_items)
    return Div(cls='wrapper').add([
        sidebar
        ,content()
    ])
code = """
$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});
"""