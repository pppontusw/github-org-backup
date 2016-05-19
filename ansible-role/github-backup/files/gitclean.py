import datetime
import os
import configparser
import shutil

try:
	parser = configparser.ConfigParser()
	parser.read('config.ini')
	bkpfolder = parser.get('CONFIG', 'CNF_BKPFOLDER')
	daystokeep = parser.get('CONFIG', 'CNF_DAYSTOKEEP')
except:
    print('config.ini is either invalid or does not exist. Please verify your config.ini file.')
    exit()

timestamp = datetime.datetime.now()
timedelta = datetime.timedelta(days=int(daystokeep))
timestamp = timestamp - timedelta
backupDirectory = os.environ['HOME'] + "/" + bkpfolder + "/" + str(timestamp.year) + str(timestamp.month) + str(timestamp.day)
backupDirectory = backupDirectory + '.tar'

def main():
	if os.path.isdir(backupDirectory):
		shutil.rmtree(backupDirectory)
	elif os.path.exists(backupDirectory):
		os.remove(backupDirectory)

if __name__ == '__main__':
	main()