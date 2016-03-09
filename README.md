# transcriber

Transcription interface for crowdsourcing experiment

## Requirements

Django

## Run Locally

The following keys are required:

|Key|Location|
|---|---|
|Django secret key | /transcriber/settings_secret.py |
|RSA public key | /tone/static/js/resume.js, /tone/static/js/survey.js |
|RSA private key | /tone/static/rsa/private_key.pem |

Log in to the admin console at /admin and change the password. The default pass word is ```P@ssw0rd```

Comment out mysqlclient in requirements.txt if not using MySQL

```pip install -r requirements.txt```

```python manage.py runserver```
