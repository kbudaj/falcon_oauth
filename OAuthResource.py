import falcon
import json
from requests_oauthlib import OAuth2Session


class AuthResource(object):
    def __init__(self, settings):
        self.settings = settings
        self.session_options = {}

        possible_session_options = {'scope', 'redirect_uri'}
        for key in settings:
            if key in possible_session_options:
                self.session_options[key] = settings[key]

    def on_get(self, req, resp):
        session = OAuth2Session(
            self.settings['client_id'], **self.session_options)
        authorization_url, state = session.authorization_url(
            self.settings['auth_uri'])
        raise falcon.HTTPMovedPermanently(authorization_url)


class AuthCallbackResource(AuthResource):
    def __init__(self, settings, callback):
        super().__init__(settings)
        self.callback = callback

    def on_get(self, req, resp):
        auth_resp_url = 'https://' + req.url.split('//')[1]
        session = OAuth2Session(
            self.settings['client_id'], **self.session_options)
        session.fetch_token(
            self.settings['token_uri'],
            client_secret=self.settings['client_secret'],
            authorization_response=auth_resp_url)
        data = session.get(self.settings['data_request_url'])
        data = json.loads(data.content)

        self.callback.execute(req, resp, data)


class Callback(object):
    def __init__(self):
        self.response = falcon.Response

    def execute(self, oauth_data):
        """ Interface like, requires implementation """
        raise NotImplementedError("Execute method requires implementation")
