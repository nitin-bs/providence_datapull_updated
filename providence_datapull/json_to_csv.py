import json
data=json.load(open('hosts.json',))
outfile=open('hosts.csv','w')
outfile.write('installationId,public_ip,auth_token,signupusername')
for i in data:
    dict_val=json.loads(i["params"])
    auth_token=dict_val["auth_token"]
    public_ip=dict_val["output"]["public_ip"]
    sign_up_user=dict_val["signUpUserName"]
    outfile.write(i['installationId']+','+public_ip+','+auth_token+','+sign_up_user+'\n')
outfile.close()    
#print(i['installationId']+','+i['params']['output']['public_ip'])
    #print("\n")
