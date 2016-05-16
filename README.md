# transcriber

Transcription interface for crowdsourcing experiment

## Requirements

Django

## Run Locally

1. Generate the secret keys not included with this git repository. The following keys are required:

  | Key | Location |
  |---|---|
  | Django secret key | /transcriber/settings_secret.py |
  | RSA public key | /tone/static/js/resume.js, /tone/static/js/survey.js |
  | RSA private key | /tone/static/rsa/private_key.pem |

2. Install python dependencies. Comment out mysqlclient in requirements.txt if not using MySQL locally.

   ```pip install -r requirements.txt```
   
3. Initialize the database

   ```python manage.py makemigrations```
   
   ```python manage.py migrate```

4. Start the server

   ```python manage.py runserver```

Log in to the admin console at /admin and change the password. Username is ```admin```, default password is ```P@ssw0rd```

The summary pages can be viewed at /tone/summary/0 and /tone/summary/1

## Deploying to Amazon Elastic Beanstalk instance

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

## Important Django files

| File | Description |
|---|---|
| tone/management/commands | Custom Django commands. Run with django-admin command |

## Important Elastic Beanstalk files

| File | Description |
|---|---|
| requirements.txt | Python requirements to be installed on the environment |
| .ebignore | Similar to .gitignore, lists files that should not be included when deploying to Elastic Beanstalk |
| .ebextensions/01-transcriber.config | List of commands to run when deploying to Elastic Beanstalk |
