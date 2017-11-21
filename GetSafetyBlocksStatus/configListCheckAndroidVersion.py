
'''
Check by configurationlist services the current 
'''
import http.client 
import json 
from collections import defaultdict
#servers
CONST_IP_SERVER_DEV="172.18.43.33"
CONST_IP_SERVER_PRE="172.18.43.20"

#SETTINGS - change it to tune
#user agent header http connection version code
arg_version_codigo_user_agent="17.6.0"
#version code
arg_version_codigo="1760"
#server API address
arg_server_ip=CONST_IP_SERVER_DEV
arg_server_ip=CONST_IP_SERVER_PRE

with open("androidVersionList.txt") as f: 
	for line in f: 
		android_versions = f.read().splitlines()

#OUTPUT HEADER
print("Servidor %s" % (arg_server_ip))
print("Desarrollo %s" % (arg_version_codigo))
print("Version\tEstado")
	
for version in android_versions:

  #init connection
	conn = http.client.HTTPConnection("%s:58380" % (arg_server_ip))
	
	headers = { 'accept-language': "es", 
	'accept': 'application/vnd.idk.bsmobil-v%s+json' % (arg_version_codigo), 
	'content-type': "application/json",
	'user-agent': "ANDROID %s Android+SDK+built+for+x86 NATIVE_APP %s STANDARD" % (version,arg_version_codigo_user_agent), 
	'cache-control': "no-cache"} 
	
	#print(headers)

  #service and url 
	conn.request("GET", "/bsmobil/api/safeblocks/configurationlist", headers=headers)

	res = conn.getresponse() 
	data = res.read()
	
	#check for eror response
	output_response=data.decode("utf-8") 
	if output_response.count('Error') > 0:
		print("Error connection query for %s" % (version))
		continue
		
	#parse json data string to object
	response=json.loads(data)
	#print(response)
	
  #create a key pair empty
	block_struct = defaultdict(lambda : None)
	
  #load blocks name and status to block_struct
  
	for block in response["blocks"]: 
		block_name=block["name"	]
		status=block["status"]
		block_struct[block_name]=status
		
  #OUTPUT results
	if(len(response["blocks"]) == 0):
		print("%s\thas empty blocks" % (version))
	else:
		for block in block_struct:
			if status == "0":
				status_str="Activado"
			else:
				status_str="Desactivado"
			print("%s\t%s" % (version,status_str))
		
	
