#!/opt/anaconda/bin/python3.6
import cgitb
cgitb.enable()
import cgi
import json
from sys import path
path.append('/home/bf7750/python/pkgs')

import postgresql as pg
from urllib.parse import parse_qs
form = cgi.FieldStorage()
print('Content-Type: text/plain\n\n')
print(json.loads(form['columns'].value))
