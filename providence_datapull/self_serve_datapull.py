import requests
import os
import sys
import json
import csv
r = csv.reader(open('/home/centos/nitin/hosts.csv'),quotechar="'") # Here your hosts csv file
lines = list()
for row in r:
    if(any(row)):
        lines.append(row)
entities=[{"collection":"sources",
           "api":"/v1.1/sources.json?",
           "path":"/home/centos/nitin/providence_datapull/data/sources/",
           "subapi":"/v1.1/source/info.json?source_id="},

{"collection":"domains",
           "api":"/v1.1/domains.json?",
           "path":"/home/centos/nitin/providence_datapull/data/domains/"},
{"collection":"jobs",
           "api":"/v1.1/jobs.json?",
           "path":"/home/centos/nitin/providence_datapull/data/jobs/"}
]
res_sources_final=[]
sources=[]
sources_json={}
for i in range(1,len(lines)):
    for entity in entities:
        auth_token=lines[i][2]
        if('+' in auth_token):
            auth_token=auth_token.replace('+','%2B')
        print('Exporting '+lines[i][1]+" "+entity["collection"])
        try:
            res = requests.get(url="http://"+lines[i][1]+":3000"+entity["api"]+"auth_token="+auth_token,timeout=10)
        except Exception as e:
            print('Error: Failed to connect to ' + lines[i][1] +' reason'+str(e))
            import traceback
            #traceback.print_exc()  
            break
        if(not os.path.exists(entity["path"])):
            os.makedirs(entity["path"])
        with open(entity["path"]+lines[i][0]+'-'+entity["collection"]+'.json','w') as entity_file:
            entity_file.write(res.text)

print("Done")



