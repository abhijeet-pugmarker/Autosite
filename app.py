#!/usr/bin/python3
import os 
import sys
import functions as fn
# Take Argument Array
all_argv= sys.argv[1:]

if(len(all_argv) > 0):
	if(all_argv[0] == 'create'):
		if(len(all_argv) == 3):
			if(all_argv[1] == 'site'):
				site_name = all_argv[2]
				if(len(site_name.split('.')) > 1 ):
					#Step 1 : Create a folder in /var/www/html/
					fn.step_one(site_name)
				else:
					print('Error. please check site name (Example: example.com)')
					
		else:
			print("autosite create site <site_name>")
	elif(all_argv[0] == 'delete'):
		if(len(all_argv) == 3):
			if(all_argv[1] == 'site'):
				site_name = all_argv[2]
				fn.delete_site(site_name)
		else:
			print("autosite delete site <site_name>")
	elif(len(all_argv) == 1):
		if(all_argv[0] == '-h' or all_argv[0] == '--help'):
			fn.myHelp()
			
	
else:
	fn.myHelp()
