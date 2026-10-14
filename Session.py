import requests
import secrets
import base64
import hashlib
import webbrowser
import time
import hmac
from dataclasses import dataclass, field
from urllib.parse import urlsplit,parse_qs

httpSession = requests.Session()
httpSession.trust_env=False

@dataclass(frozen=True)
class LoginAttempt:
    verifier:str=field(default_factory=lambda:secrets.token_urlsafe(32),repr=False)
    challenge:str=field(init=False)
    state:str=field(default_factory=lambda:secrets.token_urlsafe(16),repr=False)
    def __post_init__(self):
        digest=hashlib.sha256(self.verifier.encode()).digest()
        challenge=base64.urlsafe_b64encode(digest).decode().rstrip("=")
        object.__setattr__(self,"challenge",challenge)

def GetSessionTokenCode(loginAttempt:LoginAttempt)-> dict :
    params={
        'state':loginAttempt.state,
        'redirect_uri':'npf71b963c1b7b6d119://auth',
        'client_id':'71b963c1b7b6d119',
        'scope':'openid user user.birthday user.mii user.screenName',
        'response_type': 'session_token_code',
        'session_token_code_challenge':loginAttempt.challenge,
        'session_token_code_challenge_method': 'S256',
        'theme':'login_form'
    }
    response=httpSession.get('https://accounts.nintendo.com/connect/1.0.0/authorize?',params=params,allow_redirects=False)
    webbrowser.open(response.headers['Location'])
    callbackUrl=input().strip()
    return dict(parse_qs(urlsplit(callbackUrl).fragment))
#state,session_token_code,session_token_code_verifier

def GetSessionToken(sessionTokenCode:str,loginAttempt:LoginAttempt)->dict:
    dataSession={
        'client_id':'71b963c1b7b6d119',
        'session_token_code':sessionTokenCode,
        'session_token_code_verifier':loginAttempt.verifier
    }
    sessionToken=httpSession.post('https://accounts.nintendo.com/connect/1.0.0/api/session_token',
                                  data=dataSession,headers={'User-Agent':'Mozilla/5.0'})
    return sessionToken.json()
#session_token,code

def GetAccountToken(sessionToken:str):
    data={
        'client_id':'71b963c1b7b6d119',
        'session_token':sessionToken,
        'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
    }
    accountToken=httpSession.post('https://accounts.nintendo.com/connect/1.0.0/api/token',
                             data=data,headers={'User-Agent': 'Mozilla/5.0'})
    return accountToken.json()
#token_type,expires_in,access_token,id_token,scope

def GetUser(accessToken:str):
    headers={
        'Authorization': 'Bearer ' + accessToken,
        'User-Agent': 'Mozilla/5.0'
    }
    user=httpSession.get('https://api.accounts.nintendo.com/2.0.0/users/me',headers=headers)
    return user.json()
#..

loginAttempt=LoginAttempt()
sessionTokenCode=GetSessionTokenCode(loginAttempt)
if sessionTokenCode['state'][0]!=loginAttempt.state:
    raise RuntimeError('state 不匹配')
sessionToken=GetSessionToken(sessionTokenCode['session_token_code'][0],loginAttempt)
accountToken=GetAccountToken(sessionToken['session_token'])
user=GetUser(accountToken['access_token'])
print(loginAttempt,'\n',sessionTokenCode,'\n',sessionToken,'\n',accountToken,'\n',user)