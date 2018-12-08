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
tname = form['name'].value
columns = form['columns'].value
schema = form['schema'].value if 'schema' in form else 'public'
and_cols_in = ''
if columns!='*':
    and_cols_in = f"""
	and column_name in (
	    {','.join(["'"+c+"'" for c in columns.split(',')])}
	)
    """ 
query = f"""
    with t as (
	select 
	    replace(initcap(column_name),'_',' ') as title,
	    column_name as data,
	    data_type,
	    column_name in (
		select a.attname 
		from pg_index i 
		    join pg_attribute a 
		    on a.attrelid = i.indrelid 
			and a.attnum = any(i.indkey) 
		where i.indrelid = '{tname}'::regclass
	    ) as pkey
	from information_schema.columns 
	where 
	    table_schema='{schema}' 
	    and table_name='{tname}'
	    {and_cols_in}
    )
    select array_to_json(array_agg(t)) from  t
"""
# print(form)
# print(query)
print(db.query(query)[0][0])
