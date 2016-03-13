# transcriber

Transcription interface for crowdsourcing experiment

## Requirements

Django

## Run Locally

The following keys are required:

| Key | Location |
|---|---|
| Django secret key | /transcriber/settings_secret.py |
| RSA public key | /tone/static/js/resume.js, /tone/static/js/survey.js |
| RSA private key | /tone/static/rsa/private_key.pem |

Comment out mysqlclient in requirements.txt if not using MySQL

```pip install -r requirements.txt```

```python manage.py runserver```

Log in to the admin console at /admin and change the password. The default password is ```P@ssw0rd```

The summary pages can be viewed at /tone/summary/0 and /tone/summary/1

## Important Django files

| File | Description |
|---|---|
| tone/management/commands | Custom Django commands. Run with django-admin command |

## Important Elastic Beanstalk files

| File | Description |
|---|---|
| .ebignore | Similar to .gitignore, lists files that should not be included when deploying to Elastic Beanstalk |
| .ebextensions/01-transcriber.config | List of commands to run when deploying to Elastic Beanstalk |
