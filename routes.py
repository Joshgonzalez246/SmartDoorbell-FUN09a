from __future__ import print_function

import os.path
from flask import render_template, session, redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from . import app
from app import client_app_file, app_secret

app.secret_key = app_secret
service = None

SCOPES = [
             "https://www.googleapis.com/auth/userinfo.profile",
             "https://www.googleapis.com/auth/userinfo.email",
             "https://www.googleapis.com/auth/drive",
             "https://www.googleapis.com/auth/drive.file",
             "openid"
         ]


# index location (landing page)
@app.route("/")
def index():
    return render_template("index.html")


# login location, redirect to google auth
@app.route("/login")
def login():
    if os.path.exists('client_app/token.json'):
        os.remove('client_app/token.json')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('client_app/token.json'):
        creds = Credentials.from_authorized_user_file('client_app/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_app_file, SCOPES)
            creds = flow.run_local_server(port=8040)
        # Save the credentials for the next run
        with open('client_app/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    print(u'{0}: {1}'.format("Refresh Token", creds.refresh_token))

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, mimeType, createdTime,webViewLink)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) {2}'.format(item['name'], item['id'], item['webViewLink']))

    return render_template("index.html", files=items)


# logout, clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#
@app.route("/oncomplete")
def oncomplete():
    return redirect("/")


if __name__ == "__main.py__":
    app.run(debug=True)
