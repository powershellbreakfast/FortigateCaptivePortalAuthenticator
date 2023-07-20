#!/usr/bin/python3
import requests
import re
import time
import urllib.parse
import urllib3
import sys
import getopt
#disable request ssl verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class captive_portal_authenticator():
    def __init__(self,PASSWORD,USERNAME):
        self.password = PASSWORD
        self.username = USERNAME
        self.test_url = "https://google.com"
        self.sleeptime = 30
        self.fgt_redirect_url = ""
        self.magic = ""
        self.main()

    #main loop
    def main(self):
        while True:
            #check to see if authenticated
            is_authenticated = self.test()

            #if authentticated wait
            if is_authenticated:
                print(f"Device is authenticated, sleeping for {self.sleeptime} seconds")
                time.sleep(self.sleeptime)

            #if not authenticated, login
            else:
                self.login()
                print("login attempted")
                

    def test(self):
        #pattern to detect fortigate captive portal redirect
        fgt_captive_portal_regex = re.compile('window\.location=[\/\w\.\:\"]*fgtauth\?\w{16}\"')
        #request test webpage
        response = requests.get(self.test_url,verify=False)
        #stop if status not 200
        response.raise_for_status()
        #search the response for a redirect
        regex_search_results = fgt_captive_portal_regex.search(response.text)
        
        #if regex pattern is found in response
        if regex_search_results:
            #redirect was found, you are not authenticated
            #save the redirect url for use in the login function
            self.fgt_redirect_url = regex_search_results.group().split("=")[1].replace('"','')
            return False
        else:
            #assume you are autheticated
            return True

        

    def login(self):
        #get the login page
        response = requests.get(self.fgt_redirect_url,verify=False)
        #stop if status not 200
        response.raise_for_status()
        #set magic value 
        self.magic = self.fgt_redirect_url.split("?")[1]
        post_url = self.fgt_redirect_url.split("?")[0]
        #post login
        post_data = {
            '4Tredir':self.test_url,
            'magic':self.magic,
            'username':self.username,
            'password':self.password
        }
        #url encode post data
        encoded_data = urllib.parse.urlencode(post_data)
        #make a post attempt to login
        login_response = requests.post(post_url,data=encoded_data,verify=False)
        #stop if status not 200
        login_response.raise_for_status()


def main(argv):
    USERNAME = ''
    PASSWORD = ''
    try:
        opts, args = getopt.getopt(argv,"hu:p:",["username=","password="])
    except getopt.GetoptError:
        print ('auth.py -u <username> -p <password>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('auth.py -u <username> -p <password>')
            sys.exit()
        elif opt in ("-u", "--username"):
            USERNAME = arg
        elif opt in ("-p", "--password"):
            PASSWORD = arg

    captive_portal_authenticator(PASSWORD,USERNAME)



if __name__ == "__main__":
    main(sys.argv[1:])
