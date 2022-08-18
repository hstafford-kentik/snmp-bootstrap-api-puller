#! /usr/bin/python3

import requests
import json
import argparse
from argparse import RawTextHelpFormatter
import sys


parser = argparse.ArgumentParser(
		description='''a cli utility to retrieve devices with a given label.
- 
- Kentik email address & API token required (via arguments or set on lines 32 and 33 of the code)
- Email and API info can be found in your Kentik profile (https://portal.kentik.com/profile4/info)''', formatter_class=RawTextHelpFormatter)


# Optional Arguments
parser.add_argument('-e','--email', help='Kentik User Email', metavar='')
parser.add_argument('-a','--api', help='API key for User', metavar='')
parser.add_argument('-l','--label', help='Label to search for', metavar='')


# Create a variable that holds all the arguments
args = parser.parse_args()

# Assign email and api token supplied to variables to be used with API call
# If email and api not supplied check hardcoded variables on line 32 and 33
if args.email and args.api:
	email = args.email
	api = args.api
else:
	email = "<YOUR PORTAL EMAIL LOGIN>" 
	api = "<YOUR API KEY FROM PORTAL>" 

if args.label:
	label = args.label
else:
	label = "SNMP-Only"
	

# Create a function to make the API call and return list of deviceIDs
def data_api_call(k_email, k_api):

	# Set appropriate headers and API end-point for JSON call
	headers = {'Content-Type': 'application/json', 'X-CH-Auth-API-Token': k_api, 'X-CH-Auth-Email': k_email}
	url = 'https://api.kentik.com/api/v5/deviceLabels'

	try:
		# Use JSON requests to pull chart and assign to a variable
		response = requests.get(url, headers=headers)
		response.raise_for_status()
		data = json.loads(response.text)

		deviceList = []
		deviceNameList = []
		for labels in data:
			#print (labels['name'])
			if labels['name'] == label:
				for devices in labels['devices']:
					#print (devices['id'],devices['device_name'])
					deviceList.append([devices['id'],devices['device_name']])
		return(deviceList)

	# If error occurs with API call, print error and quit script
	except requests.exceptions.RequestException as err:
		print(err)
		print(err.response.text)
		sys.exit()


#deviceIDs = data_api_call(email, api)
deviceList = data_api_call(email, api)
IDList = ''
prefix = ''
print('Found the following devices with the label '+label)
for device in deviceList:
	print(device[0]+"\t"+device[1])
	IDList = IDList+prefix+device[0]
	prefix = ','
with open('/etc/default/snmp_device_list.env', 'w') as outFile:
    outFile.write('BOOTSTRAP_DEVICES='+IDList+'\n')
