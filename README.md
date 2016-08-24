# GamblerBackup
GamblerBackup - Simple backup system multiplatform

#Dependencies
<pre>
pip install pydrive
</pre>

#Origin
Use the file dirs.txt to put your origins folders
<pre>
/var/www
/root/project
</pre>

#Configuration
Use the file gbackup.config
<pre>
[destination]
backup_folder=/root/backup #Folder where will be stored de backup

[email]
smtp=smtp.gmail.com:587 #smtp server:port
email=email@gmail.com #E-mail to send the log
password=P4$$W0RD
subject=Backup Client Brazil #Subject of the e-mail
recpients=['email1@gmail.com','email2@gmail'] 
</pre>

#Google drive configuration
<pre>
Go to <a href="https://console.developers.google.com/iam-admin/projects">APIs Console</a> and make your own project.
Search for ‘Google Drive API’, select the entry, and click ‘Enable’.
Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:

  1.Select ‘Application type’ to be Web application.
  2.Enter an appropriate name.
  3.Input http://localhost:8080 for ‘Authorized JavaScript origins’.
  4.Input http://localhost:8080/ for ‘Authorized redirect URIs’.
  5.Click ‘Save’.

Click ‘Download JSON’ on the right side of Client ID to download client_secret_<really long ID>.json.

The downloaded file has all authentication information of your application. Rename the file to “client_secrets.json” and place it in your working directory.
</pre>

#Usage
<pre>
python gbackup.py -m full #Full backup
python gbackup.py -m incremental #Incremental Backup
python gbackup.py -m full -g enable #Full backup saving in google drive folder
python gbackup.py -s password.txt -l /root/backup #Search for a file in zip files recursively
</pre>
