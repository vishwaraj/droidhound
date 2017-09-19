import os
import requests
import argparse
import time
import schedule
from bs4 import BeautifulSoup
import sys
from sys import platform
from config import push_msg

print """ 
   ___    __                     __
  / _ \  / /  ___  __ _____  ___/ /
 / // / / _ \/ _ \/ // / _ \/ _  / 
/____/ /_//_/\___/\_,_/_//_/\_,_/  

[+]By Vishwaraj \n"""


if len(sys.argv)<3:
		print "Usage: " + sys.argv[0]+" -t,--target "+ "<package_name>"
		print "Usage: " + sys.argv[0]+" -s,--sniff  "+ "<package_name>"
		
		exit(0)

old_version=None
dict1={'package':old_version}
package=sys.argv[2]
pwd=os.getcwd()



def get_current_version(package):
	r = requests.get("http://apk-dl.com/%s" % package)
	soup=BeautifulSoup(r.text,"html.parser")
	data=soup.select('span.version')
	current_version=data[0].text

	return current_version


def get_download_link(link):

	download_link2=requests.get(link)
	download_link3=download_link2.url
	download_link4=requests.get(download_link3)
	soup=BeautifulSoup(download_link4.text,"html.parser")
	final_link=soup.find_all('a',attrs={'class':'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect fixed-size'})
	for link in final_link:
		mofo_link=link.get('href')
		return mofo_link



def operations(package_name):
	print "Deploying to the device!"
	adb(package_name)
	trigger_drozer_scan(package_name)
	return


def write_version(directory,current_version):
	os.chdir(directory)
	f=open('app_version.txt','w')
	f.write(package+":"+current_version)
	f.close()
	os.chdir(pwd)

def create_directory(directory,current_version):

	if not os.path.exists(directory):
		os.makedirs(directory)
		write_version(directory,current_version)     

def adb_install(package_name):

	os.system(adb_path+" uninstall %s"%package_name)
	os.system(adb_path+" install %s"%package_name)

def drozer_adb_support():
	# os.system("adb kill-server")
	# os.system("adb start-server")
	os.system(adb_path+" forward tcp:31415 tcp:31415")
	# os.system("drozer console connect")

def call_for_download(url):
	print "Creating the directory"
	print "Preparing to download apk...."
	os.chdir(directory)
	r = requests.get(url)

	with open(app_name_in_directory, "wb") as code:
		code.write(r.content)
	print "Apk Downloaded..."
	print "Deploying to device"	
	adb_install(app_name_in_directory)
	print "App has been installed"
	return



def trigger_drozer_scan(package_name):

	print "Running checks..."
	check_drozer_install=os.system("adb shell pm list packages | grep com.mwr.dz")
	if check_drozer_install!=0:
		print "Drozer not found!"
		print "Installing drozer...."
		os.system(adb_path+" install dz.apk")
	print "Launching app..."
	os.system(adb_path+" shell monkey -p %s  -c android.intent.category.LAUNCHER 1"%package_name)
	print "Launching drozer"		
	os.system(adb_path+" shell monkey -p com.mwr.dz -c android.intent.category.LAUNCHER 1")
	print "Drozer launched...."	
	
	print "App launched"
	print "Started Pwning..."
	os.chdir(pwd)
	os.system("python testd.py %s "%package_name)

def operations(package_name):
	print "Deploying to the device!"
	adb(package_name)
	trigger_drozer_scan(package_name)
	return

def read_previous_version():
	os.chdir(directory)
	r=open('app_version.txt','r')
	l=r.readline()
	package,version=l.split(":")
	r.close()
	return version

def hunt_mode(directory,current_version):

	print "Preparing..."
	create_directory(directory,current_version)
	call_for_download(full_url)
	print "Downloaded Apk...."
	print "Deploying to the device...."
	adb_install(app_name_in_directory)
	print "Deployed..."
	print "Started autopwn...."
	trigger_drozer_scan(package)
	write_version(directory,current_version)


def version_check(directory,current_version):

	create_directory(directory,current_version)
	oldy=read_previous_version()
	if current_version!=oldy:
		print "Version change detected"
		push_msg(package,current_version)
		print "Downloading Apk...."
		call_for_download(full_url)
		print "Downloaded Apk"
		print "Deploying to the device..."
		adb_install(app_name_in_directory)
		print "Started autopwn..."
		trigger_drozer_scan(package)
		print "Updating the version in record..."
		write_version(directory,current_version)
		return

	else:
	    print "No change detected"
	    start_sniff()

#Sniffing mode
def start_sniff():
	try:
		# scheduler = BlockingScheduler()
		# scheduler.add_job(version_check, 'interval', seconds=3,id='apksniff')
		# scheduler.start()
		schedule.every().day.at("9:00").do(version_check)

		while True :
			print "Sniffing Mode Activated"
			print "Dhound will notify about version change!"
			schedule.run_pending()
			time.sleep(60)

	except (KeyboardInterrupt, SystemExit):

		pass

def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print(errmsg)
    sys.exit()

#Preparing the url's
config_link="http://www.apkfind.com/store/download?id=%s"%package
app_name_in_directory=package+".apk"
predown_url=get_download_link(config_link)
full_url="http:"+predown_url
current_version=get_current_version(package)
directory=package

if predown_url==None:
	print "Download limit exceeded!"

if __name__== "__main__":

    #parsing the argument
	parser=argparse.ArgumentParser()
	parser.add_argument('-t','--target', help="Download and Scan the app",
                    action="store_true")
	parser.add_argument('-s','--sniff',help="Start the sniff mode",action="store_true")
	
	
	args,unknown=parser.parse_known_args()
	
	parser.error = parser_error

#Code for os check 
if platform=='win32':

                adb_path="C:\\pentdroid\\bin\\platform-tools\\adb.exe"
                pwd=os.getcwd()
                testd_path=pwd+"\\testd.py"
                directory=pwd+"\\"+package

else:
    adb_path="adb"
    directory=pwd+"/"+package


if args.target:
	
	print "Preparing..."
	print "app_version:",current_version+" Package: "+package
	hunt_mode(directory,current_version)

elif args.sniff:

	version_check(directory,current_version)



	

	

