#!/opt/anaconda/bin/python3.6
import cgitb
cgitb.enable()
import cgi
import json
from sys import path
path.append('/home/bf7750/python/pkgs')

import postgresql as pg
from urllib.parse import parse_qs

response = []
#%%  Connection
db = pg.open('pq://ben:ben@localhost:5432/crdb')
DEBUG = False
#%% Passed variables
form = cgi.FieldStorage()
#{
#	op: table._op,
#	table: table.name, 
#	form_data: $('#table_form').serialize(), 
#	columns: JSON.stringify(table._columns)
#}

op = form['op'].value
schema = form['schema'].value if 'schema' in form else 'public'
table_name = form['table'].value 
form_data = parse_qs(form['form_data'].value)
columns = json.loads(form['columns'].value)
if DEBUG:
    form = {
        'form_data': 'id=1&name=Alaska%20Communications%20Systems%20Group&iso=XX&cable_system=ACS%20Alaska-Oregon%20Network%20(AKORN)&tg_carrier_id=0&notes=.&priority=4',
        'op': 'edit',
        'columns': """
            [{
                "title":"Id"
                ,"data":"id"
                ,"data_type":"bigint"
                ,"pkey":true
                ,"sTitle":"Id"
                ,"mData":"id"
            },{
                "title":"Name"
                ,"data":"name"
                ,"data_type":"text"
                ,"pkey":true
                ,"sTitle":"Name"
                ,"mData":"name"
            },{
                "title":"Iso"
                ,"data":"iso"
                ,"data_type":"text"
                ,"pkey":false
                ,"sTitle":"Iso"
                ,"mData":"iso"
            },{
                "title":"Cable+System"
                ,"data":"cable_system"
                ,"data_type":"text"
                ,"pkey":true
                ,"sTitle":"Cable+System"
                ,"mData":"cable_system"
            },{
                "title":"Tg+Carrier+Id"
                ,"data":"tg_carrier_id"
                ,"data_type":"jsonb"
                ,"pkey":false
                ,"sTitle":"Tg+Carrier+Id"
                ,"mData":"tg_carrier_id"
            },{
                "title":"Notes"
                ,"data":"notes"
                ,"data_type":"text"
                ,"pkey":false
                ,"sTitle":"Notes"
                ,"mData":"notes"
            },{
                "title":"Priority"
                ,"data":"priority"
                ,"data_type":"integer"
                ,"pkey":false
                ,"sTitle":"Priority"
                ,"mData":"priority"
            }]""",
        'table': 'consortium_owners'
    }
    op = form['op']
    table_name = form['table']
    form_data =  parse_qs(form['form_data'])
    columns = json.loads(form['columns'])
pkeys = []
# TODO: this is a poor excuse for determining which is strings or not
for i,v in enumerate(columns):
    if (v['data_type'] in ('text','date')):
        form_data[v['data']] = f"'{form_data[v['data']][0]}'" 
    elif (v['data_type']=='jsonb'):
        jdata = form_data[v['data']][0]
        if jdata[0]!='[':
            jdata = '['+jdata
        if jdata[-1]!=']':
            jdata = jdata+']'
        form_data[v['data']] = f"to_jsonb('{jdata}'::text)" 
    else:
        form_data[v['data']] = form_data[v['data']][0]
    if (v['pkey']):    
        pkeys.append(v['data'])

#%% Add ' ' around each value that contains non-numbers
where = ' where '+' and '.join([f'{pk} = {form_data[pk]}' for pk in pkeys])

response.append('Content-Type: text/plain\n\n')
if DEBUG:
    response.append(form)

#%% Operations
if (op == 'edit'):
    cols = f"{','.join([k for k in form_data.keys() if k not in pkeys])}"
    set_values = ' , '.join([f'{k} = {v}' 
                             for k,v in form_data.items() 
                             if k not in pkeys]) 
    if DEBUG: 
        response.append(f"update {schema}.{table_name} set {set_values} {where}")
    else:
        db.execute(f"update {schema}.{table_name} set {set_values} {where}")
elif (op == 'add'):
    cols = f"{','.join([k for k in form_data.keys()])}"
    values = "("+','.join([v for v in form_data.values()])+")"
    check = f'select 1 from {schema}.{table_name} {where}'
    if DEBUG:
        response.append(check)
    if (db.query(check)):
        # response.insert(0,'Status 400: Bad request\n')
        response.append('Primary key(s) already used')
    else:
        insert_sql = f"insert into {schema}.{table_name} ({cols}) values {values}"
        if DEBUG:
            response.append(f"insert: {insert_sql}")
        else:
            db.execute(insert_sql)
else:
    del_sql = f"delete from {schema}.{table_name} {where}"
    if DEBUG:
        response.append(f"deleting: {del_sql}")
    else:
        response.append(f"deleting: {del_sql}")
        db.execute(del_sql)
#%%
# Reply with a "read" of the row.
if (op != 'del'):
    cols = f"{','.join([k for k in form_data.keys()])}"
    read_row = f"""
        with t as (select {cols} from {schema}.{table_name} {where})
        select array_to_json(array_agg(t)) from  t
    """
    response.append(db.query(read_row)[0][0])

for line in response:
    print(line)


