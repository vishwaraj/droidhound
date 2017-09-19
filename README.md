## About D-hound 

* dhound is a python tool designed to help penetration testers and bug hunters to perform quick dynamic scans on android apps right from terminal. It also keeps sniffing (working as a cron job) the change in apk version as soon as the version change is detected it will send a push notification to the user and starts scanning.

* Product security teams can also integrate or modify it accordingly to regularly scan there apk builds for vulnerability checks.

## Demo :
coming

## Dependencies :

dhound uses `bs4`, `requests`, `schedule`, and `argparse` python modules.

These dependencies can be installed using the requirements file:

- Installation on Windows:
```
c:\python27\python.exe -m pip install -r requirements.txt
```
- Installation on Linux
```
sudo pip install -r requirements.txt
```
* **ADB** : Tool helps to run operations on android 
* **Drozer** : it uses drozer as a scanning engine you will need to download it from here https://labs.mwrinfosecurity.com/tools/drozer/

## How to setup guide ? 
#### Install python 
* 2.7.x is suggested and make sure python_path is in environment variables

#### Install ADB 
* For windows setup adb from here  https://developer.android.com/studio/releases/platform-tools.html by downloading the platform tools package

#### Install drozer
* **For Windows** : https://labs.mwrinfosecurity.com/tools/drozer/
* **For Mac** : https://github.com/mwrlabs/drozer/releases/download/2.3.4/drozer-2.3.4.tar.gz or you can use quick script to install it https://github.com/vishwaraj/drozer_install

#### Install Android Emulator
* Preffered Genymotion , Leapdroid 
* Install **drozer_agent.apk** in the emulator and keep it running in the background. 

#### Finally clone it
```
git clone https://github.com/vishwaraj/droidhound.git
```
```
cd droidhound
```
## Note : 
* **You have to update adb_path (where adb is located in windows ? ) in below code which can be found in dhound.py file**
* **Similarly update drozer_path and adb_path in the below code as per your system which can be found in testd.py file**

```
# dhound.py file here please update adb_path as per your system adb location
# Code for os check
if platform=='win32':

                adb_path="C:\\pentdroid\\bin\\platform-tools\\adb.exe"
                pwd=os.getcwd()
                testd_path=pwd+"\\testd.py"
                directory=pwd+"\\"+package

else:
    adb_path="adb"
    directory=pwd+"/"+package
```

```
#In testd.py file Please update adb_path and drozer_path as located in your system

if platform=='win32':
    
	adb_path="C:\\pentdroid\\bin\\platform-tools\\adb.exe"
	drozer_path="C:\\drozer\\drozer.bat"
	save_path=pwd+"\\"+pname

else:
	adb_path="adb"
	drozer_path="drozer"
	save_path=pwd+"/"+pname
```

## Usage :

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-t            | --target      | Downloads the apk and start the scanning
-s            | --sniff       | Detects version change , sends push notifcation and starts scanning

#### if you already have any apk in your emulator and directly want's to scan then
* Start the drozer agent in emulator
* Then hit ``` python testd.py <package_name>```
* you will find the results in package folder

### Examples :

* To download and start scanning

```python dhound.py -t <package_name>```
```python dhound.py -t <com.deveoper.xyz>```

* To check and notify about version change

``python dhound.py -s <package_name>``

## License :

dhound is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT)

## Version
**Current version is 1.0**

## Contributing
**Bug reports and pull requests are welcome on GitHub at** 
https://github.com/vishwaraj/droidhound
