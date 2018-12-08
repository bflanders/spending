#!/opt/anaconda/bin/python3.6
import json
from sys import path
path.append('/home/bf7750/python/pkgs')

import postgresql as pg

#%%  Connection
db = pg.open('pq://ben:ben@localhost:5432/crdb')

#%%  Header
print("Content-Type: application/json")
print()
print()
#%% Getting data
print(json.dumps([r[0] for r in db.query("""
    select schema_name 
    from information_schema.schemata 
    where 
	left(schema_name,3) <> 'pg_' and 
    schema_name <> 'information_schema'
""")]))
