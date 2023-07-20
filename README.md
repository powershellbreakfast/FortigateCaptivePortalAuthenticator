# FortigateCaptivePortalAuthenticator
A Quick and easy python script to authenticate with a FortiGate captive portal for operating systems that dont have access to a browser or run headless.


## Download 
Download the file
```bash
wget https://raw.githubusercontent.com/powershellbreakfast/FortigateCaptivePortalAuthenticator/main/auth.py
```

## Optional: Modify
if you want to store the username and password in the script you can modify it to do so.
```bash
nano auth.py
```
At the top of the script replace `USERNAME` with your "username" and `PASSWORD` with your "password" in qoutes that you will use to login to the captive portal. The time in between authentication checks can also be configured here it is set to 30 seconds by default.
```python
class captive_portal_authenticator():
    def __init__(self,PASSWORD,USERNAME):
        self.password = PASSWORD
        self.username = USERNAME
        self.test_url = "https://google.com"
        self.sleeptime = 30
        self.fgt_redirect_url = ""
        self.magic = ""
        self.main()
```

## Execute
Execute the script.
```bash
python3 auth.py -u jimmy -p jimmypass
```
## Optional: Create a Service to run the script.
Create a new service file
```bash
sudo nano /etc/systemd/system/fgtauth.service
```
Inside the file paste this, make sure to replace `<username>` with the username of the home directory the file lives in. on my machine it was ubuntu so it would look like this `/home/ubuntu/auth.py`
```bash
[Unit]
Description=A Service that runs a python script to authenticate a linux machine to fortigate's captive web portal.
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/<username>/auth.py -u jimmy -p jimmypass
[Install]
WantedBy=multi-user.target
```
Install the service
```bash
sudo systemctl enable fgtauth.service
```
Start the service
```bash
sudo systemctl start test.service
```
