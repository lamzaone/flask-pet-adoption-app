# google-client-app
Flask, Flask-Login, Login with Google, App setup as Google Client

1.1 Installation with Pipenv:

```
pipenv install
```

1.2 Installation without Pipenv:

```
pip install -r requirements.txt
```

2. Generate a SSL certificate (on windows you can use GitBash)
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

3. Generate Google OAuth2.0 API credentials on Google Console and store them into your system environments variables


4. Initalize the database by running app.py for the first time:

```
python app.py
```

Should see "Initialized the database."

5. Run the command again to start the Flask web server locally:

```
python app.py
```
