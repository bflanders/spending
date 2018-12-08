#!/opt/anaconda/bin/python3.6
import cgi
import json
from sys import path
path.append('/home/bf7750/python/pkgs')

import postgresql as pg

#%%  Connection
db = pg.open('pq://ben:ben@localhost:5432/crdb')

#%% Passed variables
form = cgi.FieldStorage()
#%%  Header
print("Content-Type: application/json")
print()
print()
#%% Getting data
schema = form['schema'].value if 'schema' in form else 'public'
print(json.dumps([r[0] for r in db.query(f"""
    select tablename 
    from pg_tables 
    where schemaname = '{schema}'
""")]))

