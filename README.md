# google-client-app
Flask, Flask-Login, Login with Google, App setup as Google Client

Installation with Pipenv:

```
pipenv install
```

Installation without Pipenv:

```
pip install -r requirements.txt
```

Generate a SSL certificate
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Generate Google OAuth2.0 credentials and store them into your system environments variables


Initalize the database by running app.py for the first time:

```
python app.py
```

Should see "Initialized the database."

Run the command again to start the Flask web server locally:

```
python app.py
```
