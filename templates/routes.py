import google.auth.transport.requests
import requests
from flask import render_template, session, redirect, abort, request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from . import app
from app import client_app_file, GOOGLE_CLIENT_ID, app_secret

app.secret_key = app_secret

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_app_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:8040/oncomplete"
)


#index location (landing page)
@app.route("/")
def index():
    return render_template("index.html")


#login location, redirect to google auth
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


#logout, clear session
@app.route("/logout")
def logout():
    print(session)
    session.clear()
    print(session)
    return redirect("/")


#
@app.route("/oncomplete")
def oncomplete():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # Possible XSS

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_information = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    print(id_information)
    session["google_id"] = id_information.get("sub")
    session["name"] = id_information.get("name")
    return redirect("/")


if __name__ == "__main.py__":
    app.run(debug=True)
