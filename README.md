# flask app for pet adoptions with google oauth2.0 login
Flask, Flask-Login, Login with Google, App setup as Google Client

1.  Installation with Pipenv:

```
pipenv install
```

- Installation without Pipenv:

```
pip install -r requirements.txt
```

2. Generate a SSL certificate (on windows you can use GitBash)
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
- Or, instead you could replace the last line of app.py with
```python3
    app.run(ssl_context="adhoc", host='127.0.0.1', port='5000')
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


if the command above gives errors, try using python3 instead of python.
