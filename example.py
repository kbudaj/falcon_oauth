import falcon
import os
import json

from OAuthResource import AuthResource, AuthCallbackResource

GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']

GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']

google_credentials = {
    'client_id': GOOGLE_CLIENT_ID,
    'client_secret': GOOGLE_CLIENT_SECRET,
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://accounts.google.com/o/oauth2/token',
    'redirect_uri': 'http://127.0.0.1:8000/google/callback',
    'scope': ['https://www.googleapis.com/auth/userinfo.email',
              'https://www.googleapis.com/auth/userinfo.profile'],
    'data_request_url': 'https://www.googleapis.com/oauth2/v1/userinfo'
}

github_credentials = {
    'client_id': GITHUB_CLIENT_ID,
    'client_secret': GITHUB_CLIENT_SECRET,
    'auth_uri': 'https://github.com/login/oauth/authorize',
    'token_uri': 'https://github.com/login/oauth/access_token',
    'data_request_url': 'https://api.github.com/user'
}


def print_user_id(req, resp, oauth_data):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(oauth_data)
        print("-- Callback function, print_user_id --")
        print("User ID: {}".format(oauth_data['id']))
        print("--------------------------------------")


app = falcon.API()

app.add_route('/google/', AuthResource(google_credentials))
app.add_route('/google/callback', AuthCallbackResource(
    google_credentials, callback=print_user_id))

app.add_route('/github/', AuthResource(github_credentials))
app.add_route('/github/callback', AuthCallbackResource(
    github_credentials, callback=print_user_id))
