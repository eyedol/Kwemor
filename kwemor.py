from oauth import oauth
from oauthtwitter import OAuthApi

import pprint
import httplib
import socket
import re

import sys,os


class Kwemor:
    consumer_key = "yyx9XQKu3MjeudFnYbSMA"
    consumer_secrete = "pmH6FvKZptKjJ2tytY0OunzDvGfDPD0GHG0YNdU"
    oauth_token = "7415812-lTWSLvH3fTFC2lhWAtYJObBIiNze2yYvlBg3PQ9G8a"
    oauth_token_secret = "QTeyNirnXhwcZJuXYEIUocK9uGZjBc47ynQ7rWLIpwQ"
    oauth_verifier = "9822792"
    twitter = ""

    def __init__(self): # constructor
        print "Kwemore, the website monitor"
        self.authenticate_app()
    
    #authenticate user
    def authenticate_app(self):

        self.twitter = OAuthApi(self.consumer_key, self.consumer_secrete,
        self.oauth_token, self.oauth_token_secret)
        user_timeline = self.twitter.GetUserTimeline();
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(user_timeline)
    # print how to use kwemor from the commandline
    def usage(self):
        print 'Usage: Kwemor \n\tpython kwemor.py --<arguments>\n\n\tArguments'
        print '\t\t--adduser:\n\t\tuse this option to add a new user.'
        print '\n\t\te.g: python kwemore.py --adduser <twitter_username>\n\n'
        print '\t\t--auth:\n\t\tuse this option to authenticate the kwemor app.'
        print '\n\t\te.g: python kwemor.py --auth \n\n' 

    
    # send DM to users 
    def post_dm(self):
        text = 'Your website is so up Mr.'
        for user in self.read_lines('users.txt'):
            if not user == "":
                dm = self.twitter.SendDM(user,text)

        # user = 'lorenzocabrini'
        # text = 'Your website is so up Mr.'
        # dm = self.twitter.SendDM(user,text)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(dm)
    
    # send http get request to see if a website is up
    def send_http_req(self,url, path='/'):
        try:
            conn = httplib.HTTPConnection(url)
            conn.request("HEAD", path)
            if re.match("^[23]\d\d$", str(conn.getresponse().status)):
                return True
        except StandardError:
            return None
    
    def is_website_online(host):
        try:
            socket.gethostbyname(host)
        except socket.gaierror:
            return False
        else:
            return True

    # Read content of a file
    def read_lines(self, path):
        f = open(path, 'r')
        content = f.readlines()
        
        f.close()
        
        return content
    
    #write content to a file
    def write_lines(self, content):
        path = 'users.txt'    
        # recreate a new file and append the content to it
        f = open(path, 'a')
        f.write(content)
        f.close()
        
    #add a new user
    def add_user(self,username):
        self.write_lines(username)

        print "User %s" % username + " added."

    def remove_user(self):
        content = self.read_lines('users.txt')
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(content)

if __name__ == '__main__':
    kwemor = Kwemor()
    
    x = len(sys.argv)
    
    if x < 3:
        kwemor.usage()
    
    else:
        if sys.argv[1] == '--adduser': # --add a new user
            kwemor.add_user(sys.argv[2]) 
   
        elif sys.argv[1] == '--dm': # --post a dm
            kwemor.post_dm()

        elif sys.arg[1] == '--rmuser': # --remove an user
            kwemor.remove_user()

        else:
            print "Error: Unknown argument\n"
            kwemor.usage()
