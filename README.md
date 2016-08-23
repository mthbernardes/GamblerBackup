# GamblerBackup
GamblerBackup - Simple backup system multiplatform

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

#Usage
<pre>
python gbackup.py -m full #Full backup
python gbackup.py -m incremental #Incremental Backup
python gbackup.py -s password.txt -l /root/backup #Search for a file in zip files recursively
</pre>
