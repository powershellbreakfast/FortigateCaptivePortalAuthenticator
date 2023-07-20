# FortigateCaptivePortalAuthenticator
A Quick and easy python script to authenticate with a FortiGate captive portal for operating systems that dont have access to a browser or run headless.


## Download 
Download the file
```bash
wget https://raw.githubusercontent.com/powershellbreakfast/FortigateCaptivePortalAuthenticator/main/auth.py
```

## Modify
```bash
nano auth.py
```
At the top of the script replace jimmy with your username and password you will use to login to the captive portal with. The time in between authentication checks can also be configured here it is set to 30 seconds by default.
```python
class captive_portal_authenticator():
    def __init__(self):
        self.password = "jimmy"
        self.username = "jimmy"
        self.test_url = "https://google.com"
        self.sleeptime = 30
        self.fgt_redirect_url = ""
        self.magic = ""
        self.main()
```

## Execute
Execute the script.
```bash
python3 auth.py
```
Optionally: Create a Service to run the script.
```bash

```
