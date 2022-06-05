# PyPhish
## The Python Phishing Framework to test resilience against Phishing Campaigns

#### This framework allows to simulate phishing campaigns, in order to test the resilience and the cyber awareness of the targets. It is possible to choose distinct phishing templates, that will be used as pretext to induce users to click on the embedded link. 
#### A second component is the Command and Control server, which is an HTTP server where the users will land if they click on the link embedded in the mail. The tester will be able to see who clicked on the link, since a custom URL is provided to each target. A use case is an organization targeting its employees: this way, it will be able to know exactly who clicked on the link. Then, more sophisticated C2 server could be provided, that could, for instance, display fake login pages to steal users credentials or provide drive-by downloads to test a scenario where a user downloads malware trough a malicious URL, therefore assessing the effectiveness of the security softwares installed on the target hosts.

## Usage

`usage: pyphish.py [-h] [-P PASSWORD] [-t TEMPLATE] [-v] SENDER_EMAIL SMTP_SERVER TARGETS`

positional arguments:
  SENDER_EMAIL          The sender email address (e.g.: user@example.com)
  SMTP_SERVER           The SMTP fully qualified name together with the port, in the following format:<FQDN:PORT> (ex: smtp.example.com:587). If a port is not
                        provided, it will default to 587.
  TARGETS               A comma separated receivers email addresses (e.g.: user1@example.com,user2@example.com,user3@example.com) or the PATH of a configuration
                        file. A configuration file is a CSV file holding information about the phishing targets. It is made of three columns:'Email', 'Name' and
                        'Template'. The email is necessary, while the 'Name' and 'Template' fields are optional. In case a name is associated with an email, it
                        will allow to build more user-tailored phishing emails. 'Template' allow to specify specific phishing emails for each target. Allowed
                        values are the following: <google|linkedin>.

options:
  -h, --help            show this help message and exit
  -P PASSWORD, --password PASSWORD
                        The password needed to connect the sender to the SMTP server. If not provided,user will be prompted to insert it interactively.
  -t TEMPLATE, --template TEMPLATE
                        Specifies which phishing emails will be used for all the targets. Allowed values are the following: <google|linkedin>. If you want so
                        specify distinct phishing emails for distinct targets, the receivers configuration file has to be used. If not specified, a random email
                        template is chosen.
  -v, --verbose         Displays verbose message, such as the list of targets together with the chosen templates.

PyPhish: the Python Phishing Framework Author: Francesco Balzano License: MIT