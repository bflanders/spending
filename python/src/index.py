#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:20:37 2018

@author: ben
"""

#%% Imports
from sys import path
project = 'spending'
usr = 'pi'
path.append(f'/home/{usr}/projects/{project}/lib/python/pkgs')
from element import JS, CSS, HTML, Head, Body, Code
path.append(f'/home/{usr}/projects/{project}/python/pkgs')
from compositions import default_body as body, code
#%% Sources
css_hrefs = [
    '/lib/datatables/datatables.min.css'
    ,'/lib/fontawesome/css/all.min.css'
    #,'/lib/scrollbar/css/styles.css'
    ,f'/projects/{project}/css/styles.css'
]
csss = [CSS(href=fn) for fn in css_hrefs]
js_srcs = [
    '/lib/datatables/datatables.min.js'
    ,'/lib/component/js/component.js'
    #,'/lib/scrollbar/js/scrollbar.js'
    #,'/crdb/js/composition.js'      
    ,f'/projects/{project}/js/main.js'
    #,'/crdb/js/ui.js'
]
jss = [JS(src=fn) for fn in js_srcs]

#%% Make document
# HTML
#   Head
#       CSS
#       JS
#   Body
#       Container -> row
#           Sidebar -> Menu
#           Main
head = Head(title='Databasing').add(csss+jss)
li_items = [
    ('Setting','cog')
    ,('Refresh','sync')
    ,('Add','plus-circle')
]
brand_info = ('Spending', 'file-invoice-dollar')
init_code = "$(document).ready(function(){ app.init(); }); "
doc = HTML().add([head, Body().add(Code(src=init_code))])
print(doc.html())
#%% Write out
out_dir = f'/home/{usr}/projects/{project}/web/app/html/'       
with open(out_dir+'index.html','w') as f:
    f.write(doc.html())
    f.write('<!-- Auto generated from ./python/src/index.py -->')
    
#%% Baseline
body = Body().add([body(brand_info, li_items), Code(src=code)])
doc = HTML().add([head, body])    
with open(out_dir+'index_baseline.html','w') as f:
    f.write(doc.html())
    f.write('<!-- Auto generated from ./python/src/index.py -->')
