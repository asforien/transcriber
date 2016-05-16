# transcriber

Transcription interface for crowdsourcing experiment

## Requirements

Python
Django
pip package manager

## Run Locally

1. Optional: Create a virtual environment for the project. https://virtualenv.pypa.io/en/latest/

   ```pip install virtualenv```
   
   ```virtualenv transcriber-env```
   
   ```source transcriber-env/bin/activate```

2. Generate the secret keys not included with this git repository. The following keys are required:

  | Key | Location |
  |---|---|
  | Django secret key | /transcriber/settings_secret.py |
  | RSA public key | /tone/static/js/resume.js, /tone/static/js/survey.js |
  | RSA private key | /tone/static/rsa/private_key.pem |

3. Install python dependencies. Comment out mysqlclient in requirements.txt if not using MySQL locally.

   ```pip install -r requirements.txt```
   
4. Initialize the database

   ```python manage.py makemigrations```
   
   ```python manage.py migrate```

5. Start the server

   The default location for the website is localhost:8000. This can be changed by adding an argument. 

   ```python manage.py runserver```
   
   ```python manage.py runserver 192.168.1.123:8000```

Log in to the admin console at /admin and change the password. Username is ```admin```, default password is ```P@ssw0rd```

The summary pages can be viewed at /tone/summary/0 and /tone/summary/1

## Using Amazon Elastic Beanstalk

1. Install the AWS EB Command Line Interface, available as a pip package

   ```pip install awsebcli```

2. Set up awsebcli with your AWS credentials

   ```eb init```
   
3. Create a new Elastic Beanstalk environment

   ```eb create -db```
   
   The -db flag creates an Amazon RDS MySQL database associated with the EB environment.

4. Deploy the project to the environment

   This command deploys the latest git commit if a git repository has been initialized. Uncomitted changes will not be deployed. Untracked files will be deployed.

   ```eb deploy```
   
5. Download a copy of the database

   Configure the EC2 security group associated with the database to accept inbound MySQL requests from port 3306 and any source. Then, run the following command with the correct RDS_ENDPOINT, USERNAME (default is ebroot) and PASSWORD.

   ```mysqldump ebdb -h RDS_ENDPOINT -u USERNAME -pPASSWORD -P 3306 > rds.sql```
   
6. Terminate the EB environment and associated database.

   ```eb terminate```
   
Some actions can also be performed from the web console. https://console.aws.amazon.com/

## Important Django files

| File | Description |
|---|---|
| tone/management/commands | Custom Django commands. Run with django-admin command |

## Important Elastic Beanstalk files

| File | Description |
|---|---|
| requirements.txt | Python requirements to be installed on the environment |
| .ebignore | Files that will not be  deployed to Elastic Beanstalk |
| .ebextensions/01-transcriber.config | Commands to run when deploying to Elastic Beanstalk |
