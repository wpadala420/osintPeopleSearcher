#!/usr/bin/python
import urllib
from selenium import webdriver
from time import *
import sys, signal
import argparse
import os

def main():
	numberOfPhotos=0
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--numberOfPhotos', help='Number of photos that you want to download')
	parser.add_argument('-u', '--username', help='Username of your victim in Instagram')
	args = parser.parse_args()
	if (not args.username):
		print "*******Parameter -u is required******"
		exit(0)
	if (not args.numberOfPhotos):
		print "Number of photos should be specified"
		exit(0)

	username = args.username
	numberOfPhotos = int(args.numberOfPhotos)

	url = 'https://www.instagram.com/'+username+'/?hl=en'
	driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
	driver.get(url)

	aas = driver.find_elements_by_tag_name('a')
	for i in aas:
		if (i.get_attribute('innerHTML')=='Load more'):
			i.click()
			print "Load more is clicked"
			sleep(2)
	while (len(driver.find_elements_by_tag_name('img'))-10<numberOfPhotos):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(1)

	sleep(2)
	img = driver.find_elements_by_tag_name('img')
	s=1
	os.makedirs(username)
	for i in img:
		if (numberOfPhotos==0):
			break
		urllib.urlretrieve(i.get_attribute('src'), username+'/'+str(s)+'.jpg')
		numberOfPhotos-=1
		s+=1
		#print i.get_attribute('src')

	driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
	driver.quit()

if __name__ == '__main__':
    main()
