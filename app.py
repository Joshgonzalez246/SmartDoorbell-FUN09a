import os
import pathlib
import flask

app = flask.Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # for debugging
client_app_file = os.path.join(pathlib.Path(__file__).parent, "client_app/client_secret_nat_app.json") #file containing app information
GOOGLE_CLIENT_ID = "691499918272-79hnmhfp1vm384tiksang7dm15d5v4p8.apps.googleusercontent.com" # google client id
app_secret = "969874774268"

if __name__ == "__main.py__":
    app.run(debug=True)

@app.route('/')
def index():
    if google_auth.is_logged_in():
        drive_fields = "files(id,name,mimeType,createdTime,modifiedTime,shared,webContentLink)"
        items = google_drive.build_drive_api_v3().list(
                        pageSize=20, orderBy="folder", q='trashed=false',
                        fields=drive_fields
                    ).execute()

        return flask.render_template('list.html', files=items['files'], user_info=google_auth.get_user_info())

    return 'You are not currently logged in.'
