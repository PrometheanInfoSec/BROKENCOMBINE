#!/usr/bin/env python


#Number of iterations of SHA256 to run. 
#Must be same as number used in add_record.py (when records were added)
ITERATIONS = 500

#We need a username and password to a gmail to send the emails with
#If these two lines and the sento line aren't set the alert will just log to log.txt and do nothing else.
email=''
password=''

#We will need something to do with the alert
#You can set an email address to send the alert to
#Or you can try sending the alert to a phone number
sendto=''

#If you put in a phone number you'll need to tell me what carrier it is on.
carrier=''

#NOTE
"""you may need to set your gmail account to work with insecure apps.  Just google for the current instructions at your time of reading this.  It's super easy."""
#NOTE

import BaseHTTPServer, SimpleHTTPServer
import ssl
from urlparse import parse_qs
import pip
import smtplib

try:
	from Crypto.Hash import SHA256
except:
	pip.main(['install',"pycrypto"])
	from Crypto.Hash import SHA256

convert = {"verizon":"vtext.com","tmobile":"tmomail.net","at&t":"txt.att.net","alltel":"message.alltel.com","ampd":"vtext.com","boost":"myboostmibile.com","cingular":"mobile.mycingular.com","cricket":"mms.mycricket.com","einstein":"einsteinmms.com","nextel":"messaging.nextel.com","sprint":"messaging.sprintpcs.com","suncom":"tms.suncom.com","voicestream":"voicestream.net","uscellular":"email.uscc.net","virgin":"vmobl.com","rogers":"sms.rogers.com","fido":"fido.ca","telus":"msg.telus.com","bell":"txt.bell.ca","kudo":"msg.koodomobile.com","mts":"text.mtsmobility.com","presidents":"txt.bell.ca","sasktel":"sms.sasktel.com","solo":"txt.bell.ca","virginca":"vmobile.ca"}

def send_alert(msg):
	global sendto
	if "@" not in sendto:
		sendto = sendto + "@" + convert['carrier']

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(email,password)
	server.sendmail(email,sentdo,msg)
	server.quit()

def log(msg):
	fi = open("log.txt","a")
	fi.write(msg+"\n")
	fi.close()

def alert(parsed):
	alertstring = "User %s has triggered an alert by entering their password insto an unstrusted form." % parsed["user"]
	if len(email) > 1 and len(password) > 1 and len(sendto) > 1:
		send_alert(alertstring)
	log(alertstring)
	

def check_pass(parsed, line, user=None):
	pazz = parsed['pass']
	for i in range(ITERATIONS):
		h=SHA256.new()
		h.update(pazz)
		pazz = h.hexdigest()

	if pazz == line[1].strip():
		if user is not None:
			parsed['user'] = user
		alert(parsed)

def read_in_data():
	fi = open("passwd.txt","r")
	data = fi.read()
	fi.close()
	return data

def process(parsed):
	data = read_in_data()
	for line in data.split("\n"):
		if len(line) < 1:
			continue
		line = line.split(":")
		if "user" in parsed:
			if line[0].strip() == parsed["user"]:
				check_pass(parsed, line)
			else:
				continue
		else:
			check_pass(parsed, line, user=line[0].strip())
			

def parse(path):
	parsed = parse_qs(path[2:])
	if "pass" in parsed:
		for i in parsed:
			parsed[i] = " ".join(parsed[i])
		print parsed
		process(parsed)
		return True
	return False

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		if parse(self.path):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("INPUT RECEIVED")
		else:
			self.send_error(404, 'File not found')
		return


if __name__ == "__main__":

	try:
		httpd = BaseHTTPServer.HTTPServer(('',4443),
		Handler)
		httpd.socket = ssl.wrap_socket(httpd.socket,
		certfile='cert.pem', keyfile="cert.key", server_side=True)
		httpd.serve_forever()
	except KeyboardInterrupt:
		print 'SIGINT received, shutting down web server'
		httpd.socket.close()
