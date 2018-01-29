import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import configparser
import json
from urllib.parse import urlparse, parse_qs
import subprocess
#import string

hostName = ""
hostPort = 80
serviceidentifier = "/areyouashroombox"
boxidentifier = "/getboxid"
landingpage = "lp.html"
setupcompletehtml = "setupcomplete.html"
setupwifi = "/setupwifi"
HTML_START = "<!DOCTYPE html><html>"
HTML_END = "</html>"

supplicant_file_template = "wpa_supplicant_t.conf"
supplicant_file_target = "wpa_supplicant_temp.conf"
TAG_SSID = "<SSID>"
TAG_PSW = "<PSW>"

ERROR_CODE_INVALID_LENGTH = {'code':"1000", "msg":"Invalid data length"};
ERROR_CODE_PSW_NO_MATCH = {'code':"1001", "msg":"Password fields do not match"};
ERROR_CODE_INVALID_DATA = {'code':"1002", "msg":"Invalid data"};
SUCCESS_CODE = {'code':"2000", "msg":"Success"};

class ConfigReader:
	def openconfig(self):
		config = configparser.ConfigParser()
		config.read('bid.cfg')
		return config
		
	def getboxid(self):
		config = self.openconfig()
		return config.get("bid", "identifier")
 
	def getpassword(self):
		config = self.openconfig()
		return config.get("bid", "psw")

class MyServer(BaseHTTPRequestHandler):

	#	GET is for clients geting the predi
	def do_GET(self):
		self.send_response(200)
		if self.path == serviceidentifier:
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes("yes","utf-8"));
		elif self.path == boxidentifier:
			config = ConfigReader();
			identifier = config.getboxid()
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes(identifier,"utf-8"));
		elif self.path == setupwifi:
			f = open("setupwifi.html", 'rb')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		else:
			f = open("lp.html", 'rb')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			#self.wfile.write(bytes("ShroomKeeper ShroomBox","utf-8"));

		
		#self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
		

	#	POST is for submitting data.
	def getMessage(self, mappd, dictmess):
		retval = dictmess['msg']
		if("mobapp" in mappd):
			retval = dictmess['code'];
		return retval;

	def do_POST(self):

		print( "incomming http: ", self.path )

		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		post_data_s = post_data.decode("utf-8");
		#self.wfile.write(post_data)
		#mappd = parse_qs(urlparse(post_data_).query);
		mappd = parse_qs(post_data_s);
		#print(post_data)
		print(mappd)
		if ("ssid" in mappd) and ("p1" in mappd) and ("p2" in mappd):
			#print(len(mappd["ssid"][0]))
			if (len(mappd["ssid"][0]) >  3) and (len(mappd["p1"][0]) > 3) and (len(mappd["p2"][0]) > 3):
				if mappd["p1"][0] == mappd["p2"][0]:
					#self.wfile.write(bytes("ready to setup", "utf-8"))
					f = open(supplicant_file_template, 'rb')
					templatedata = f.read().decode("utf-8");
					f.close()
					#TAG_SSID, TAG_PSW
					targetdata = templatedata.replace(TAG_SSID, mappd["ssid"][0])
					targetdata = targetdata.replace(TAG_PSW, mappd["p1"][0])
					target = open(supplicant_file_target, "wb+");
					target.write(bytes(targetdata,"utf-8"))
					target.close();
					subprocess.Popen(["./setupwifi.sh"])
					print(targetdata)
					if("mobiapp" in mappd):
						self.wfile.write(bytes(SUCCESS_CODE["code"],"utf-8"));
					else:
						f = open(setupcompletehtml, 'rb')
						self.wfile.write(f.read())
						f.close()
				else:
					message = self.getMessage(mappd, ERROR_CODE_PSW_NO_MATCH);
					self.wfile.write(bytes(message, "utf-8"))
			else:
				message = self.getMessage(mappd, ERROR_CODE_INVALID_LENGTH);
				self.wfile.write(bytes(message, "utf-8"))
		else:
			message = self.getMessage(mappd, ERROR_CODE_INVALID_DATA);
			self.wfile.write(bytes(message, "utf-8"))
 
		

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
