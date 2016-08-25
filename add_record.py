#!/usr/bin/env python

try:
	from Crypto.Hash import SHA256
except:
	import pip
	pip.main(['install','pycrypto'])
	from Crypto.Hash import SHA256

user = raw_input("Please enter the username: ")
pazz = raw_input("Please enter the password: ")

for i in range(500):
	h = SHA256.new()
	h.update(pazz)
	pazz = h.hexdigest()

fi = open("passwd.txt","a")
fi.write(user+":"+pazz)
fi.close()

print "User entry added to passwd.txt"

