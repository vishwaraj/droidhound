import subprocess
import os
import shutil
import sys
from sys import platform
from time import gmtime, strftime

pname=sys.argv[1]

if len(sys.argv)<1:
		print "Usage: " + sys.argv[0]+ "<package_name>"
		exit(0)

pwd=os.getcwd()


# Code for os check
if platform=='win32':
    
	adb_path="C:\\pentdroid\\bin\\platform-tools\\adb.exe"
	drozer_path="C:\\drozer\\drozer.bat"
	save_path=pwd+"\\"+pname

else:
	adb_path="adb"
	drozer_path="drozer"
	save_path=pwd+"/"+pname



def write_version(directory):
	os.chdir(directory)
	f=open('app_version.txt','w')
	f.write(pname+":"+"version")
	f.close()
	os.chdir(pwd)

def create_directory(directory):

	if not os.path.exists(directory):
		os.makedirs(directory)
		write_version(directory) 

last_time=strftime("%d-%m-%Y %H:%M:%S", gmtime())

html = "<html><head><title>Report: %s</title></head><body><h2>%s</h2>Last scanned: %s " % (pname,pname,last_time)

html+="""
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>

"""

create_directory(pname)

def drozer_checks():

	print "Running checks..."
	check_drozer_install=os.system("adb shell pm list packages | grep com.mwr.dz")
	if check_drozer_install!=0:
		print "Drozer not found!"
		print "Installing drozer...."
		os.system(adb_path+" install dz.apk")
		os.system(adb_path+" shell monkey -p com.mwr.dz -c android.intent.category.LAUNCHER 1")
		print "Drozer Launched"

def drozer_adb_support():

	os.system("%s kill-server"%adb_path)
	os.system("%s start-server"%adb_path)
	os.system("%s forward tcp:31415 tcp:31415"%adb_path)
	# os.system("drozer console connect")
	return

def execute_test(test,pname):
  drozer_cmd = '%s console connect -c "%s  %s "' %(drozer_path,test, pname)
  process = subprocess.Popen(drozer_cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)# subprocess.call('drozer console connect -c "%s -a %s "' % (test, package), shell = True)# subprocess.call('drozer console connect -c "%s  %s "' % (test2, package), shell = True)
  input, output, error = process.stdin, process.stdout, process.stderr
  data = output.read().decode('latin1')
  input.close()
  print data
  output.close()
  status = process.wait()
  if int(data.find("could not find the package"))!=-1:
  	data = "Invalid package"
  else:
  	pass
  
  return data

def process_data(heading, out):
	
	html_out = 1
	separator = ("*"*50)
	print "\n%s:\n%s\n%s" % (heading,separator,out)
	out = out.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\\n","<br>").replace("\\r","")
	if html_out:
		global html
		html += """<table class="table"><tbody><tr><td><pre style=''>"""+out+"""</pre></td></tr><tr><td><thead class="thead-inverse"><br><tr><th>"""+heading+"""</th></td></tr></thead></tbody></table>"""
	
if __name__ == '__main__':
	
	
	drozer_adb_support()
	# pname = sys.argv[1]
	separator = ("*"*50)
	#Get package information
	package_info = execute_test('run app.package.info -a', pname)
	process_data("Package Information", package_info)
	#Get activity information
	activity_info = execute_test('run app.activity.info -i -u -a', pname)
	process_data("Activities Information", activity_info)
	#Get broadcast receiver information
	broadcast_info = execute_test('run app.broadcast.info -i -u -a', pname)
	process_data("Broadcast Receivers Information", broadcast_info)
	#Get attack surface details
	attacksurface_info = execute_test('run app.package.attacksurface', pname)
	process_data("Attack Surface Information", attacksurface_info)
	#Get package with backup API details
	backupapi_info = execute_test('run app.package.backup -f', pname)
	process_data("Package with Backup API Information", backupapi_info)
	#Get Android Manifest of the package
	manifest_info = execute_test('run app.package.manifest', pname)
	process_data("Android Manifest File", manifest_info)
	#Get native libraries information
	nativelib_info = execute_test('run app.package.native', pname)
	process_data("Native Libraries used", nativelib_info)
	#Get content provider information
	contentprovider_info = execute_test('run app.provider.info -u -a', pname)
	process_data("Content Provider Information", contentprovider_info)
	#Get URIs from package
	finduri_info = execute_test('run app.provider.finduri', pname)
	process_data("Content Provider URIs", finduri_info)
	#Get services information
	services_info = execute_test('run app.service.info -i -u -a', pname)
	process_data("Services Information", services_info)
	#Get native components included in package
	nativecomponents_info = execute_test('run scanner.misc.native -a', pname)
	process_data("Native Components in Package", nativecomponents_info)
	#Get world readable files in app installation directory /data/data/<package_name>/
	worldreadable_info = execute_test('run scanner.misc.readablefiles /data/data/'+pname+'/', pname)
	process_data("World Readable Files in App Installation Location", worldreadable_info)
	#Get world writeable files in app installation directory /data/data/<package_name>/
	worldwriteable_info = execute_test('run scanner.misc.readablefiles /data/data/'+pname+'/', pname)
	process_data("World Writeable Files in App Installation Location", worldwriteable_info)
	#Get content providers that can be queried from current context
	querycp_info = execute_test('run scanner.provider.finduris -a', pname)
	process_data("Content Providers Query from Current Context", querycp_info)
	#Perform SQL Injection on content providers
	sqli_info = execute_test('run scanner.provider.injection -a', pname)
	process_data("SQL Injection on Content Providers", sqli_info)
	#Find SQL Tables trying SQL Injection
	sqltables_info = execute_test('run scanner.provider.sqltables -a', pname)
	process_data("SQL Tables using SQL Injection", sqltables_info)
	#Test for directory traversal vulnerability
	dirtraversal_info = execute_test('run scanner.provider.traversal -a', pname)
	process_data("Directory Traversal using Content Provider", dirtraversal_info)
	html += "</body></html>"
	os.chdir(save_path)
	f = open("%s.html"%pname,"w")
	f.write(html)
	f.close()
	print "[*] '%s.html' with testing results saved"%pname


