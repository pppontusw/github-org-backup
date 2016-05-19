# Github Organization Backup Tool

Make sure your account has an SSH key set up to clone repos

Make a config.ini with below:

```
[CONFIG]
# Your github username
CNF_USERNAME=githubuser
# A personal auth key to access github
CNF_PASS=$OAUTHKEY$
# Your organization name
CNF_ORGNAME=githuborg
# The folder to backup to (in your home folder)
CNF_BKPFOLDER=githubbackups
```
And run the script (manually once to accept host key of github.com) or cron it to make daily backups for example, but make sure to do:

```ssh-keyscan github.com >> ~/.ssh/known_hosts```
