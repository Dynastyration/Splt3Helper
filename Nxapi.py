import Http
import base64
def GetNSOConfig() -> str:
    '''
    x.x.x
    '''
    response = Http.httpSession.get('https://nxapi-znca-api.fancy.org.uk/api/znca/config',
        timeout=(20, 30)).json()
    return response['nso_version']

def GetNxapiToken()->dict:
    '''
    access_token,token_type.expires_in,scope,refresh_token
    '''
    body={
        'grant_type': 'client_credentials',
        'client_id':'4CBp2BanFQCwlzr9SEPX4Q',
        'scope': 'ca:gf ca:er ca:dr'
    }
    nxapiToken=Http.httpSession.post('https://nxapi-auth.fancy.org.uk/api/oauth/token',
        data=body,
        timeout=(20, 120)
    )
    return nxapiToken.json()
def GetNxapiF(NxapiaccessToken:str,NSidToken:str,usernaId:str,userlanguage:str,NSOVersion:str)->dict:
    '''
    f,timestamp,request_id
    '''
    header={
        'Authorization':'Bearer '+NxapiaccessToken,
        'User-Agent':'Splt3Helper/0.1 (+https://github.com/Dynastyration/Splt3Helper)',
        'X-znca-Platform': 'Android',
        'X-znca-Version': NSOVersion,
        'X-znca-Client-Version': 'd8fAZDPzwimzQ7c6'
    }
    data={
        'hash_method': '1',
        'token': NSidToken,
        'na_id': usernaId,
        'encrypt_token_request': {
            'url': 'https://api-lp1.znc.srv.nintendo.net/v4/Account/Login',
            'parameter': {
                'naIdToken': NSidToken,
                'language':  userlanguage,
                'timestamp': 0,
                'requestId': '',
                'f':         ''
        }}}
    nxapiF=Http.httpSession.post('https://nxapi-znca-api.fancy.org.uk/api/znca/f',
        headers=header,
        json=data,
        timeout=(20, 120))
    # print(nxapiF.headers.get('Server-Timing'))
    # print(nxapiF.headers.get('X-Trace-Id'))
    # print(nxapiF.status_code)
    # print(nxapiF.text)
    # print(nxapiToken,'\n',nxapiF)
    return nxapiF.json()






def DecryptNXAPI(nxapiAccessToken:str,NSOCrypt:str,NSOVersion)->dict:
    '''
    ...
    '''
    decryptResp=Http.httpSession.post('https://nxapi-znca-api.fancy.org.uk/api/znca/decrypt-response',
    headers={
        'Authorization':'Bearer '+nxapiAccessToken,
        'User-Agent':'Splt3Helper/0.1 (+https://github.com/Dynastyration/Splt3Helper)',
        'X-znca-Platform': 'Android',
        'X-znca-Version': NSOVersion,
        'X-znca-Client-Version': 'd8fAZDPzwimzQ7c6',
        'Content-Type': 'application/json',
        'Accept': 'text/plain',},
    json={'data': base64.b64encode(NSOCrypt.content).decode()},timeout=(30,120))
    return decryptResp.json()
    
def GetNSOCoralToken(encryptedBody,nxapiAccessToken:str,NSOVersion:str)->dict:
    '''
    .....
  
    '''
    header={
        'X-Platform':       'Android',
        'X-ProductVersion': NSOVersion,
        'Content-Type':     'application/octet-stream',
        'Accept':           'application/octet-stream,application/json',
        'Connection':       'Keep-Alive',
        'Accept-Encoding':  'gzip',
        'User-Agent':       f'com.nintendo.znca/{NSOVersion}(Android/14)',}
    NSOCoralToken=Http.httpSession.post('https://api-lp1.znc.srv.nintendo.net/v4/Account/Login',\
                                   headers=header,data=encryptedBody,timeout=(30,30))
    # print(f'Coral status: {NSOCoralToken.status_code}, {len(NSOCoralToken.content)} 字节')
    # print(NSOCoralToken.text)
    return DecryptNXAPI(nxapiAccessToken,NSOCoralToken,NSOVersion)
def GetNxapiF2(nxapiAccessToken:str,coralAccessToken:str,naId:str,coralUserId:str,NSOVersion:str):
    header={
                'Authorization':'Bearer '+nxapiAccessToken,
                'User-Agent':'Splt3Helper/0.1 (+https://github.com/Dynastyration/Splt3Helper)',
                'X-znca-Platform': 'Android',
                'X-znca-Version': NSOVersion,
                'X-znca-Client-Version': 'd8fAZDPzwimzQ7c6'
            },
    body={
            "hash_method": "2",
            "token": coralAccessToken,
            "na_id": naId,
            "coral_user_id": str(coralUserId),
            'encrypt_token_request': {
                'url': 'https://api-lp1.znc.srv.nintendo.net/v4/Game/GetWebServiceToken',
                'parameter': {
                    'id': 4834290508791808,
                    'registrationToken': '',
                    'timestamp': 0,
                    'requestId': '',
                    'f':         ''}}}
    fResp=Http.httpSession.post('https://nxapi-znca-api.fancy.org.uk/api/znca/f',
                                        headers=header,json=body,timeout=(30,120))
    return fResp.json()