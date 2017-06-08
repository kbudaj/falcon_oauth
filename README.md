# falcon_oauth
Simple Falcon Resource to reduce OAuth implementation boilerplate. 


## Usage

You need all required credentials for specific OAuth service.
For example, Google requires:

 * client_id
 * client_secret
 * auth_url
 * token_uri
 * redirect_uri
 * scope
 
 and additional setting required by this lib:
 * data_request_url
 
 which is an url to the endpoint, that provides user data.
 
 ### Example 
```python
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
```
\
You need to write callback function, that will accept 3 parameters:
* request
* response
* oauth_data

Request and response, are passed from resource, and you can use them like in Falcon resource class. 
oauth_data is a dict of values, that was returned by data_request_url.

### Example
```python
def print_user_id(request, response, oauth_data):
	response.status = falcon.HTTP_200
    response.body = json.dumps(oauth_data)
    print("User ID: {}".format(oauth_data['id']))
```
\
Then, all you need is to add two routes.\
First one is the endpoint that will invoke authorization request.\
The other, is a callback, that you need to register in your app settings.\
You should follow proper documentation.\
(Google: https://developers.google.com/identity/protocols/OAuth2)

### Example
```python
app.add_route('/google/', AuthResource(google_credentials))
app.add_route('/google/callback', AuthCallbackResource(
    google_credentials, callback=print_user_id))
```
\
All this examples, makes working code. You can check it inside `examples` directory.
