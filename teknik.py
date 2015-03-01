#!/usr/bin/env python3

from datetime import datetime
from subprocess import call
import os
import sys
from sys import exit
import configparser

try:
	import requests
except ImportError:
	print("Could not import a required module - is python-requests installed?")
	exit()

def readConfig():
	path = sys.path[0]
	config = configparser.ConfigParser()
	config.read(path+'/slopy.cfg')
	image_dir = config.get('config', 'image_dir')
	image_format = config.get('config', 'image_format')
	date_format = config.get('config', 'date_format')
	return (image_dir, image_format, date_format)

def getImage():
	image_dir, image_format, date_format = readConfig()
	date_stamp = (datetime.now().strftime(date_format)+(image_format))
	file_uri = image_dir+date_stamp 
	call(["maim", "-s", file_uri])

	return (file_uri)


def main():
	

	upload = getImage()
	payload = {'file':open(upload, "rb")}
	try:
		response = requests.post("https://api.teknik.io/upload/post",files=payload)
	except Exception as e:
		print("Error uploading {0}".format(e))
		exit()
	print (response.text.split('"')[7])
	outurl = "https://u.teknik.io/"+response.text.split('"')[7]

	local = upload.split('/')
	local = (local[-1] if len(local) > 1 else local[0])


	sys.stdout.write(outurl)
	sys.exit()

#	print(local + " -> " + remote)
#	print("copied to clipboard maybe??")

if __name__ == '__main__':
	main()
