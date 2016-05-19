import httplib2
import datetime
import json
import base64
import subprocess
import os
from ConfigParser import SafeConfigParser
import tarfile
import shutil

try:
	parser = SafeConfigParser()
	parser.read('config.ini')
	bkpfolder = parser.get('CONFIG', 'CNF_BKPFOLDER')
	orgname = parser.get('CONFIG', 'CNF_ORGNAME')
	username = parser.get('CONFIG', 'CNF_USERNAME')
	password = parser.get('CONFIG', 'CNF_PASS')
except:
    print('config.ini is either invalid or does not exist. Please verify your config.ini file.')
    exit()

FNULL = open(os.devnull, 'w')
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
	tar = tarfile.open(backupDirectory + '.tar', 'w')
	os.chdir(backupDirectory)
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
		repodir = backupDirectory + '/' + repo
		sproc = subprocess.call(["git", "clone", 'git@github.com:' + orgname + '/' + repo], stdout=FNULL)
		tar.add(repo)
	tar.close()
	if os.path.isdir(backupDirectory):
		shutil.rmtree(backupDirectory)
	elif os.path.exists(backupDirectory):
		os.remove(backupDirectory)

if __name__ == '__main__':
	main()