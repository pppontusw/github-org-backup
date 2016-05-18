import httplib2
import datetime
import json
import base64
import subprocess
import os
from ConfigParser import SafeConfigParser

try:
	parser = SafeConfigParser()
	parser.read('config.ini')
	bkpfolder = parser.get('CONFIG', 'CNF_BKPFOLDER')
	orgname = parser.get('CONFIG', 'CNF_ORGNAME')
	username = parser.get('CONFIG', 'CNF_USERNAME')
	password = parser.get('CONFIG', 'CNF_PASS')
except:
    print('config.ini is either invalid or does not exist. Please verify your config.ini file.')


timestamp = datetime.datetime.now()
backupDirectory = os.environ['HOME'] + "/" + bkpfolder + "/" + str(timestamp.year) + str(timestamp.month) + str(timestamp.day)

def main():
	try:
		os.makedirs(backupDirectory)
	except OSError:
		print('folder probably already exists')
	http = httplib2.Http()
	auth = base64.b64encode(username + ':' + password)
	c = 'h'
	count = 1
	repos = []
	while (c != []):
		r, c = http.request('https://api.github.com/orgs/' + orgname + '/repos?page=' + str(count), 
			'GET', 
			headers = { 'Authorization' : 'Basic %s' % auth })
		count += 1
		c = json.loads(c)
		for i in c:
			repos.append(i['name'])
	for repo in repos:
		print('cloning ' + 'git@github.com:' + orgname + '/' + repo)
		sproc = subprocess.Popen(["git", "clone", 'git@github.com:' + orgname + '/' + repo, backupDirectory + '/' + repo], stdout=subprocess.PIPE)
		sproc.stdout.readlines()

if __name__ == '__main__':
	main()
