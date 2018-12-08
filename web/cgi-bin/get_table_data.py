#!/opt/anaconda/bin/python3.6
import cgi
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
tname = form['name'].value
columns = form['columns'].value if 'columns' in form else '*'
where = 'where '+form['where'].value if 'where' in form else ''
limit = 'limit '+form['limit'].value if 'limit' in form else ''
query = f"""
    with t as (
	    select {columns} from {schema}.{tname}
	    {where}
	    {limit}
    )
    select array_to_json(array_agg(t)) from  t
"""
# print(form)
# print(query)
print(db.query(query)[0][0].encode('ascii', 'replace').decode('ascii'))
