import configure
import requests
from urlparse import parse_qsl

class OAuth(object):

    REDIRECT_URI = "https://www.facebook.com/connect/login_success.html"
    ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
    DEBUG_TOKEN_URL = "graph.facebook.com/debug_token"

    @classmethod
    def get_access_token(klass):
        params = {"client_id" : configure.app_id,
                  "client_secret" : configure.app_secret,
                  "code" : configure.oauth_code,
                  "redirect_uri" : klass.REDIRECT_URI
                  }
        return klass.get_access_token_with_params(params)

    @classmethod
    def get_app_token(klass):
        params = {"client_id" : configure.app_id,
                  "client_secret" : configure.app_secret,
                  "grant_type" : "client_credentials"
                  }
        return klass.get_access_token_with_params(params)

    @classmethod
    def get_access_token_with_params(klass, params):
        r = requests.get(klass.ACCESS_TOKEN_URL, params=params)
        if r.status_code != 200:
            return r
        resp_params = parse_qsl(r.text)
        resp_dict = {}
        for param in resp_params:
            resp_dict[param[0]] = param[1]
        return resp_dict        

    @classmethod
    def debug_token(klass, access_token, app_token):
        params = {"input_token" : access_token,
                  "access_token" : app_token
                  }
        r = requests.get(klass.DEBUG_TOKEN_URL, params=params)
        if r.status_code != 200:
            return r
        return r.json()
