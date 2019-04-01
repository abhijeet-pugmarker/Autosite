#!/usr/bin/python3
import os 
import sys
import subprocess
import time
#from goto import with_goto


#Functions
def myHelp():
	print('Help\n--------')
	print('autosite --help OR -h')
	print('autosite create site <site_name>')
	print('autosite delete site <site_name>')
	print('\n')
#@with_goto
def step_one(site_name):
	#Step 1 : Create a folder in /var/www/html/
	start_install = False
	site_path = '/var/www/html/'+site_name+'/public_html/'
	if(os.path.exists('/var/www/html/')):
		if(os.path.exists('/var/www/html/'+site_name)):
			
			dir_override = input('Already have a directory ? Are you want to override or not ? (Yes | No): ').lower()
			if(dir_override == 'yes' or dir_override == 'y'):
				print('Removing Directory...')
				#Remove Directory
				remove_directory='rm -r /var/www/html/'+site_name
				time.sleep(3)
				change_permission_to_current_user='sudo chown -R $USER:$USER '+site_path
				os.system(change_permission_to_current_user)
				os.system(remove_directory)
				step_one(site_name)
			elif(dir_override == 'no' or dir_override == 'y'):
				print('Alright. Stopping autosite.')
				start_install = False
				exit
			else:
				print('Wrong Input valid options are (Yes or No)')
				start_install = False
				step_one(site_name)
				
				
		else:
			create_folder='mkdir -p /var/www/html/'+site_name+'/public_html/'
			create_log_folder='mkdir -p /var/www/html/'+site_name+'/logs/'
			time.sleep(2)
			print('Creating Directory...')
			os.system(create_folder)
			print('Creating Log Directory...')
			os.system(create_log_folder)
			time.sleep(2)
			print('Directory created at /var/www/html/'+site_name+'/public_html/')
			print('Log directory created at /var/www/html/'+site_name+'/logs/')
			#Setting Permissions
			time.sleep(2)
			print('Setting Permissions...')
			ownership='sudo chown -R $USER:$USER '+site_path
			#ownership='sudo chown -R www-data:www-data '+site_path
			os.system(ownership)
			start_install = True
			
		if(start_install == True): #Start Install
			#LABEL
			#label .begin
			check=True
			while check:
				
				install_wordpress_or_not = input('Are you want to install wordpress setup (Yes | No): ').lower()
				if(install_wordpress_or_not == 'yes' or install_wordpress_or_not == 'y'):
					#Call Install Wordpress Function
					install_wordpress(site_name,site_path)
					check=False
				elif(install_wordpress_or_not == 'no' or install_wordpress_or_not == 'y'):
					#Call Install Simple Setup
					install_simple(site_name,site_path)
					check=False
				else:
					print('Wrong Input. Valid options are (Yes or No)')
					check=True
					#GOTO
					#goto .begin
		
	else:
		print('Directory /var/www/html not found.\nMake sure you have installed LAMP on your system.')


def install_wordpress(site_name,site_path):
	wp_cli_path='/usr/local/bin/wp'
	if(os.path.exists(wp_cli_path)):
		#os.system('wp core download')
		print('Installing Wordpress setup please wait...')
		wp_install = 'wp core download --path='+site_path
		wp_install_sp = subprocess.Popen(wp_install,stdout=subprocess.PIPE,shell=True)
		(wp_install_res,wp_install_err) = wp_install_sp.communicate()
		if(wp_install_res):
			print('Wordpress site installed.')
			#change ownership to www-data
			os.system('sudo chown -R www-data:www-data '+site_path)
			setup_sites_available_conf(site_name,site_path)
	else:
		print('Installing WP-CLI..')
		wp_cli_install_1 = 'curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar'
		wp_cli_install_1_sp = subprocess.Popen(wp_cli_install_1,stdout=subprocess.PIPE,shell=True)
		(wp_cli_install_1_res,wp_cli_install_1_err) = wp_cli_install_1_sp.communicate()
		os.system('php wp-cli.phar --info')
		os.system('sudo chmod +x wp-cli.phar')
		os.system('sudo mv wp-cli.phar /usr/local/bin/wp')
		os.system('wp --info')
		print('\nWP-CLI is installed successfully.')
		install_wordpress(site_name,site_path)
	
		
def install_simple(site_name,site_path):
	time.sleep(2)
	print('Setting up with index.html')
	index = open(site_path+'index.html','w')
	index.write("<h1>Thanks for using AutoSite.")
	index.close()
	time.sleep(2)
	print('Uploaded index.html file at '+site_path+'index.html')
	setup_sites_available_conf(site_name,site_path)
	
def setup_sites_available_conf(site_name,site_path):
	site_available_path='/etc/apache2/sites-available/'
	site_enabled_path='/etc/apache2/sites-enabled/'
	if(os.path.exists(site_available_path)):
			#print('Creating Configuration file in /etc/apache2/sites-available/')
			conf_file_path=site_available_path+site_name+'.conf'
			conf_enabled_path=site_enabled_path+site_name+'.conf'
			if(os.path.exists(conf_file_path)): #Check file is exists in /etc/apache2/sites-available/
					if(os.path.exists(conf_enabled_path)): #Check file is exists in /etc/apache2/sites-enabled/
						#Available + Enabled
						check=True
						while check:
							remove_conf_file = input('Configure file is already enabled.\nAre you want to disable and remove it ?? (Yes | No): ').lower()
							if(remove_conf_file == 'yes' or remove_conf_file == 'y'):
								time.sleep(1)
								print('Removing...')
								disable_site='sudo a2dissite '+site_name+'.conf'
								disable_site_sp=subprocess.Popen(disable_site,stdout=subprocess.PIPE,shell=True)
								(is_site_disabled,error_site_disabled) = disable_site_sp.communicate()
								if(is_site_disabled):
									os.system('sudo rm -r '+conf_file_path) # Remove conf file from sites-available directory
									time.sleep(1)
									print('Configuring site files...')
									setup_sites_available_conf(site_name,site_path)
									check=False
								else:
									print('Not able to disable the site.')
							elif(remove_conf_file == 'no' or remove_conf_file == 'n'):
								print('Working on it.')
								check=False
							else:
								print('Wrong Input.')
								check=True
							
								
							
					else:
						#Only Available in available
						print('Available folder only')
			else:
				server_admin="admin@"+site_name
				server_name=site_name
				server_alias="www."+site_name
				document_root=site_path
				error_log='/var/www/html/'+site_name+'/logs/error.log'
				custom_log='/var/www/html/'+site_name+'/logs/access.log combined'
				os.system('sudo touch '+conf_file_path)
				os.system('sudo chown -R $USER:$USER '+conf_file_path)
				#by default 644 and root
				os.system('sudo chmod -R 755 '+conf_file_path)
				conf_file_content='''
#Start AutoSite				
<VirtualHost *:80>
    ServerAdmin {server_admin}
    ServerName {server_name}
    ServerAlias {server_alias}
    DocumentRoot {document_root}
    ErrorLog {error_log}
    CustomLog {custom_log}
</VirtualHost>
#End AutoSite
				'''.format(
				server_admin=server_admin,
				server_name=server_name,
				server_alias=server_alias,
				document_root=document_root,
				error_log=error_log,
				custom_log=custom_log
				)
				conf_file=open(conf_file_path,'w+')
				conf_file.write(conf_file_content)
				conf_file.close()
				os.system('sudo chown -R root:root '+conf_file_path)
				os.system('sudo chmod -R 644 '+conf_file_path)
				#os.system('sudo a2ensite '+site_name+'.conf')
				enble_site_cmd='sudo a2ensite '+site_name+'.conf'
				enable_site_sp=subprocess.Popen(enble_site_cmd,stdout=subprocess.PIPE,shell=True)
				(is_site_enabled,error_enabled_site) = enable_site_sp.communicate()
				if(is_site_enabled):
						if(os.path.isfile('/etc/apache2/sites-enabled/000-default.conf')):
							ask_to_disable_000=input('Are you want to disable 000-default.conf file ?? (Yes | No): ').lower()
							if(ask_to_disable_000 == 'y' or ask_to_disable_000 == 'yes'):
								disable_000_site_cmd='sudo a2dissite 000-default.conf'
								disable_000_site_sp=subprocess.Popen(disable_000_site_cmd,stdout=subprocess.PIPE,shell=True)
								(is_site_disabled,error_disabled_site) = disable_000_site_sp.communicate()
								if(is_site_disabled):
									print('000-default.conf disabled successfully.')
								else:
									print('Unable to disable 000-default.conf')
						
							
						os.system('sudo service apache2 restart')
						time.sleep(2)
						print('Apache Server Restarted...')
						time.sleep(2)
						site_ip=input('Enter site ip address to add in /etc/hosts file: ')
						if(is_valid_site_ip(site_ip)):
							
							if site_name in open('/etc/hosts').read():
								time.sleep(2)
								print('ServerName is already exists in /etc/hosts. You can manually update your /etc/hosts file.\nReady to go.Cheers!')
							else: 
								time.sleep(2)
								print('Adding site to /etc/hosts')
								os.system('sudo chmod 777 /etc/hosts')
								update_etc_hosts=open('/etc/hosts','a+')
								new_host= site_ip+'\t'+site_name
								update_etc_hosts.write('\n#Site added by AutoSite\n'+new_host+'\n')
								update_etc_hosts.close()
								os.system('sudo chmod 644 /etc/hosts')
								time.sleep(1)
								print('/etc/hosts is updated.\nReady to go.Cheers!')
						else:
							print('Plese enter valid ip address')
						
				else:
					print('Error while enabling site..')
				
				
#Check valid site IP
def is_valid_site_ip(site_ip):
	site_ip_split= site_ip.split('.')
	if(len(site_ip_split) == 4):
		return True
	else:
		return False
		
def delete_site(site_name):
	if(os.path.exists('/var/www/html')):
		if(os.path.exists('/var/www/html/'+site_name)):
			confirm_remove= input('Are you sure to remove site permenently ? (Yes | No): ').lower()
			if(confirm_remove == 'yes' or confirm_remove == 'y'):
				if(os.path.isfile('/etc/apache2/sites-enabled/'+site_name+'.conf')):
					print('Disabling site...')
					time.sleep(1)
					disable_site='sudo a2dissite '+site_name+'.conf'
					disable_site_sp=subprocess.Popen(disable_site,stdout=subprocess.PIPE,shell=True)
					(disable_ok,disable_err) = disable_site_sp.communicate()
					if(disable_ok): 
						print('Site disabled...')
						delete_available='sudo rm -r /etc/apache2/sites-available/'+site_name+'.conf'
						os.system(delete_available)
						delete_site='sudo rm -r /var/www/html/'+site_name+'/'
						os.system(delete_site)
						os.system('sudo service apache2 restart')
						time.sleep(2)
						print('Success: Site removed. Please remove your site address from hosts file (/etc/hosts).')
						
			else:
				print('You cancelled process to remove site.')
		else:
			print('Error: Site directory not found !')
	else:
		print('Error: Make sure apache server is installed. /var/www/html not found !')
		
