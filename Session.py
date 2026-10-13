import requests
import secrets
import base64
import hashlib
import webbrowser
import json

TOKEN_FILE = 'config.json'
DIRECT = requests.Session()
DIRECT.trust_env=False

def PKCE():
    verifier=secrets.token_urlsafe(32)
    bytes=verifier.encode()
    hasher=hashlib.sha256(bytes).digest()
    challenge = base64.urlsafe_b64encode(hasher).decode().rstrip('=')
    state = secrets.token_urlsafe(16)
    return verifier,challenge,state
verifier,challenge,state=PKCE()

params={
    'state':state,
    'redirect_uri':'npf71b963c1b7b6d119://auth',
    'client_id':'71b963c1b7b6d119',
    'scope':'openid user user.birthday user.mii user.screenName',
    'response_type': 'session_token_code',
    'session_token_code_challenge':challenge,
    'session_token_code_challenge_method': 'S256',
    'theme':'login_form'
}
response=DIRECT.get('https://accounts.nintendo.com/connect/1.0.0/authorize?',params=params,allow_redirects=False)
loginUrl = response.headers['Location']
webbrowser.open(loginUrl)

callbackUrl=input().strip()
pairs = dict(item.split('=', 1) for item in callbackUrl.split('#', 1)[1].split('&'))
data={
    'client_id':'71b963c1b7b6d119',
    'session_token_code':pairs['session_token_code'],
    'session_token_code_verifier':verifier
}
token=DIRECT.post('https://accounts.nintendo.com/connect/1.0.0/api/session_token',data=data,headers={'User-Agent':'Mozilla/5.0'})
with open(TOKEN_FILE,'w',encoding='utf-8') as file:
    json.dump(token.json(),file,ensure_ascii=False,indent=2)