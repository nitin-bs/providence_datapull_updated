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
           "subapi":"/v1.1/source/info.json?source_id=",
           "subentity_path":"/home/centos/nitin/providence_datapull/data/source_detailed/"},

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
            if(entity["collection"]=="sources"):
                res_sources_json=json.loads(res.text)
                res_sources_list=res_sources_json["result"]
                for source in res_sources_list:
                    sources.append(source["id"]["$value"])
                #print(sources)
                res_source_json_val=[]
                for source_val in sources:
                    res_sources=requests.get(url="http://"+lines[i][1]+":3000"+entity["subapi"]+source_val+"&auth_token="+auth_token,timeout=5) 
                    res_source_json=json.loads(res_sources.text)
                    res_source_json['installation_id']=lines[i][0]
                    res_source_json['Signupusername']=lines[i][3]
                    res_source_json_val.append(res_source_json)
                if(not os.path.exists(entity["subentity_path"])):
                    os.makedirs(entity["subentity_path"])
                with open(entity["subentity_path"]+lines[i][0]+'-'+entity["collection"]+'_detail.json','w') as source_out:
                    source_out.write(str(res_source_json_val))
                    
               # print(res_sources_final)
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



