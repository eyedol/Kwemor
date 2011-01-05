#! /usr/bin/env python

from oauth import oauth
from oauthtwitter import OAuthApi

from httplib import HTTPConnection, socket
from smtplib import SMTP
from optparse import OptionParser, OptionValueError

import sys,os, logging


class Kwemor:
    #TODO:// make it possible to read these sensitive info from a config file instead
    consumer_key = ""
    consumer_secrete = ""
    oauth_token = ""
    oauth_token_secret = ""
    oauth_verifier = ""
    twitter = ""
    parser = ''
    
    def __init__(self): # constructor
        print "Kwemor, the website monitor"
            
    #authenticate twitter
    def authenticate_app(self):
        self.twitter = OAuthApi(self.consumer_key, self.consumer_secrete,
        self.oauth_token, self.oauth_token_secret)
        user_timeline = self.twitter.GetUserTimeline();
       
    # send DM to users 
    def post_dm(self,text):
        #authenticate twitter 
        self.authenticate_app()

        for user in self.read_lines('users.txt'):
            if not user == "":
                dm = self.twitter.SendDM(user,text)

    # Read content of a file
    def read_lines(self, path):
        f = open(path, 'r')
        content = f.readlines()
        f.close()
        
        return content
    
    #write content to a file
    def write_lines(self, content, path):
        # recreate a new file and append the content to it
        f = open(path, 'a')
        f.write(content)
        f.close()
        
    #add a new user
    def add_user(self,username):
        self.write_lines(username,'users.txt')
        print "User %s" % username + " added."
    
    #send status of a website via email notifications
    def email_alert(self,message, status,emailaddress):
        #TODO:// Read these from a config file
        username = ""
        password = ""
        fromaddress = ''
        toaddress = emailaddress

        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddress, toaddress, 'Subject: %s\r\n%s' % (status, message))
        server.quit()

    #get status of a website
    def get_website_status(self,url):
        response = self.get_response(url)
        
        try:
            status_code = getattr(response, 'status')
            if status_code in (200,302):
                return 'up'
        except AttributeError:
            pass
        return 'down'

    #get the response from the website
    def get_response(self,url):
        '''Return response object form URL'''
        try:
            conn = HTTPConnection(str(url))
            conn.request("HEAD", "/")
            return conn.getresponse()
        except socket.error:
            return None
        except:
            logging.error('Bad URL: %s' % url)
            exit(1)

    #get url headers
    def get_headers(self,url):
        response = self.get_response(url)
        try:
            return getattr(response, 'getheaders')
        except AttributeError:
            return 'Headers unavailable'

    # check website state
    def check_website(self,url):
        status = self.get_website_status(url)
        status_msg = '%s is %s' % (url,status)
    
        if status == 'down':
            ''' email and DM tweet '''
            self.email_alert(str(self.get_headers(url)), status_msg,
                    '')
            self.post_dm(status_msg)
            logging.error('%s' % status_msg)
        else:
            logging.error('%s' % status_msg)

    #fetch url from a file
    def get_urls_from_file(self,filename):
        try:
            return self.read_lines(filename)
        except:
            logging.error('Unable to read %s' % filename)
            return []

    #add an url to a file
    def add_url(self,url):
        self.write_lines(url,'urls.txt')
        print "User %s" % (url + " added.")

    # get cmd options
    def get_command_line_options(self):
        '''Sets up optparse and command line options'''
        usage = "Usage: %prog [options] url"
        version = "%prog 1.0"
        self.parser = OptionParser(usage=usage,version=version)
        self.parser.add_option("-a","--adduser",
                dest="adduser",help="Add a new twitter handle")
        self.parser.add_option("-f", "--from-file", dest="fromfile",
                help="Import urls from a text file separated by newline.")
        self.parser.add_option("-u","--addurl", dest="addurl",
                help="Add a new URL to the URL file")

        return self.parser.parse_args()

def main():
    # Get argument flags and command options
    kwemor = Kwemor()
    (options,args) = kwemor.get_command_line_options()

    urls = args

    if options.fromfile:
        urls = kwemor.get_urls_from_file(options.fromfile)

    elif options.adduser:
        kwemor.add_user(options.adduser)

    elif options.addurl:
        kwemor.add_url(options.addurl)

    else:
        urls = args

    for url in urls:
        kwemor.check_website(url.strip("\r\n"))

if __name__ == '__main__':
    main()

