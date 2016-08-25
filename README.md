#BROKENCOMBINE

This is a proof of concept tool to protect end users against credential harvesting attacks.

The tool comes in two parts

1. A server which listens for password data

2. A chrome extension which watches for forms

Heres the flow.

* Use add_record.py to add a username:password combo to passwd.txt
* Load the extension located in extension.zip into chrome
* Visit a page with an input of type "password".
* If the page is not in the whitelist (as specified in the extension's "contentscript.js"); then
* The extension will take whatever is entered and forward it via https to the server
* The server will check to see if it has a username:password combo matching the entered data.
* If it does it will trigger an alert (email/text) and also log the alert to log.txt
* Then you as the security ninja can respond however you see fit.

So, if an end user with the extension installed is attacked credential harvester style, you as the security team will know in a matter of seconds and be able to disable network access, honeypot the attackers... etc.


###THIS TOOL IS A POC
It is not ready for prime time yet.
