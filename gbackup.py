import zipfile
import os
import argparse
import logging
import ast
import smtplib
import mimetypes
import email
import email.mime.application
from datetime import datetime
from ConfigParser import ConfigParser

def environment(backup_type):

    day, month= datetime.now().strftime("%d"),datetime.now().strftime("%B")
    backup_folder = os.path.join(configs['backup_folder'],month,day)
    backup_file = 'backup_%s.zip' % backup_type
    backup_log = os.path.join(backup_folder,'backup.log')

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    logging.basicConfig(format='%(asctime)s %(message)s',filename=backup_log,level=logging.DEBUG)
    backup_zip = zipfile.ZipFile(os.path.join(backup_folder,backup_file),'w')
    return backup_folder,backup_zip,backup_log

def directorys():
    directorys = open('dirs.txt')
    for directory in directorys:
        files(directory.strip())
    backup_zip.close()

def files(directory):
    for folder,subfolders,filenames in os.walk(directory):
        for filename in filenames:
            filename = os.path.join(folder,filename)
            backup_incremental(filename)

def backup_full(filename):
    try:
        backup_zip.write(filename)
        msg = '%s - OK' % filename
        result['success'] += 1
        logging.info(msg)
    except Exception as e:
        msg = 'Backup file %s exited with the error %s' %(filename,str(e))
        result['fail'] += 1
        logging.warning(msg)

def backup_incremental(filename):
    modified = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%d-%m-%Y')
    if int(datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%d')) >= int(datetime.now().strftime("%d"))-2:
        print '%s - OK' % filename
        try:
            backup_zip.write(filename)
            msg = '%s - OK' % filename
            result['success'] += 1
            logging.info(msg)
        except Exception as e:
            msg = 'Backup file %s exited with the error %s' %(filename,str(e))
            result['fail'] += 1
            logging.warning(msg)

def sendemail():
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = '%s %s' % (configs['subject'],datetime.now().strftime("%d/%B/%Y"))
    msg['From'] = configs['email']
    msg['To'] = ','.join(ast.literal_eval(configs['recpients']))
    body = email.mime.Text.MIMEText(msg['Subject'])
    msg.attach(body)

    fp=open(backup_log,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="log")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=backup_log)
    msg.attach(att)

    s = smtplib.SMTP(configs['smtp'])
    s.starttls()
    s.login(configs['email'],configs['password'])
    s.sendmail(configs['email'],ast.literal_eval(configs['recpients']), msg.as_string())
    s.quit()

def search(search_file,location):
    for folder,subfolders,filenames in os.walk(location):
        for filename in filenames:
            if filename.endswith('.zip'):
                filename = os.path.join(folder,filename)
                zipado = zipfile.ZipFile(filename).namelist()
                for arq in zipado:
                    if search_file in arq:
                        print filename

def configuration():
    parser = ConfigParser()
    parser.read('gbackup.config')
    configs = dict()
    configs['backup_folder'] = parser.get('destination', 'backup_folder')
    configs['smtp'] =  parser.get('email', 'smtp')
    configs['email'] =  parser.get('email', 'email')
    configs['password'] =  parser.get('email', 'password')
    configs['subject'] = parser.get('email', 'subject')
    configs['recpients'] =  parser.get('email', 'recpients')

    return configs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GBackup.')
    parser.add_argument('-m', '--mode', action = 'store', dest = 'mode',required = False, help = 'Type of backup full/incremental')
    parser.add_argument('-s', '--search', action = 'append', dest = 'search', required = False, help = 'filename to search')
    parser.add_argument('-l', '--location', action = 'append', dest = 'search', required = False, help = 'Location to search files')
    args = parser.parse_args()

    if args.mode:
        result = {'success':0,'fail':0}
        backup_type = args.mode
        configs = configuration()
        backup_folder,backup_zip,backup_log = environment(backup_type)
        directorys()
        msg = '\tSuccess: %d \t\t Fail: %d' %(result['success'],result['fail'])
        logging.info(msg)
        sendemail()
    elif args.search:
        if len(args.search) == 2:
            search(args.search[0],args.search[1])
