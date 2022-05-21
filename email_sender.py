import csv, datetime, smtplib, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
        
def parse_vulnerabilities_csv(after_date="1970-01-01", filename="known_exploited_vulnerabilities.csv"):
    """ 
    Takes the vulnerabilities in the csv file {filename} and returns a list with all the vulnerabilities
    disclosed after {after_date}
    """
    vulnerabilities = []
    date_threshold = datetime.strptime(after_date, '%Y-%m-%d')
    with open (filename, 'r') as csvfile:
        vulns = csv.reader(csvfile, delimiter=',')
        for vuln in vulns: 
            if vuln[0] == 'cveID': continue #skip first title row
            date_added = datetime.strptime(vuln[4], '%Y-%m-%d')
            if (date_added >= date_threshold):
                cve = vuln[0]
                vendor = vuln[1]
                product = vuln[2]
                vname = vuln[3]
                action = vuln[6]
                ddate = vuln[7]
                v = {'CVE': cve, 'Vendor' : vendor, 'Product':product, 'VName':vname, 'Action':action, 'DDate':ddate}
                vulnerabilities.append(v)
    return vulnerabilities
    
def send_emails(sender, receivers, subject, vulnerabilities, sender_psw):
    """ Sends the emails to the proper receivers """
    sender_email = sender
    receivers_email = receivers  
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email 
    message["To"] = ", ".join(receivers_email)

    # Create the plain-text and HTML version of your message
    text = """\
        Plain text. If you are seeing this message, it means that HTML emails are not supported.
    """
    
    html = """\
    <html>
    <head>
    <style>
    .styled-table thead tr {
        background-color: #FF4136;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #FF4136;
    }
    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #FF4136;
    }
    </style>
    </head>
      <body>
        <p><h4>
        Please, check the latest exploited vulnerabilities released by CISA and carry out the requested actions before the due date.<br><br></h4>
        </p>
        <table class="styled-table" style="{
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }">
        <thead>
            <tr>
                <th>CVE</th>
                <th>Vendor/Project</th>
                <th>Product</th>
                <th>Vulnerability Name</th>
                <th>Action</th>
                <th>Due Date</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for vuln in vulnerabilities:
        html += """
            <tr>
                <td><b><b>{CVE}</b></td>
                <td><b>{Vendor}</b></td>
                <td><b>{Product}</b></td>
                <td><b>{VName}</b></td>
                <td><b>{Action}</b></td>
                <td><b>{DDate}</b></td>
            </tr>
        """.format(CVE=vuln['CVE'], Vendor=vuln['Vendor'], Product=vuln['Product'], VName=vuln['VName'], Action=vuln['Action'], DDate=vuln['DDate'])            
            
    html += """\
        </tbody>
      </table>      
      <h5><b>Kind Regards,<br>
      thebytemachine.com</b></h5>
      </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Send email
    with smtplib.SMTP('smtp.email.com', 587) as server: #replace with address of SMTP server
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_psw)
        try:
            server.sendmail(sender_email, receivers_email, message.as_string()        )
        finally:
            server.quit()
   
if __name__ == '__main__':
    sender = 'sender@email.com' #Replace with sender email address
    receivers  = ['receiver@email.com'] #Replace with sender email address
    subject = 'KNOWN EXPLOITED VULNERABILITIES CATALOG - UPDATE'
    sender_psw = getpass.getpass()
    print('Parsing vulnerabilities file ... \n')
    vulnerabilities = parse_vulnerabilities_csv(after_date="2022-05-01")
    print('Sending emails ... \n')
    send_emails(sender, receivers, subject, vulnerabilities, sender_psw)
