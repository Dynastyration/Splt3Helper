import Session
import Nxapi
import base64
def main():
    loginAttempt=Session.LoginAttempt()
    print('loginAttempt:',loginAttempt)
    print('-')
    sessionTokenCode=Session.GetSessionTokenCode(loginAttempt)
    print('sessionTokenCode:',sessionTokenCode)
    print('-')
    if sessionTokenCode['state'][0]!=loginAttempt.state:
        raise RuntimeError('ERROR:state 不匹配')
    sessionToken=Session.GetSessionToken(sessionTokenCode['session_token_code'][0],loginAttempt)
    print('sessionToken:',sessionToken)
    print('-')
    NSToken=Session.GetAccountToken(sessionToken['session_token'])
    print('accountToken:',NSToken)
    print('-')
    user=Session.GetUser(NSToken['access_token'])
    print('userinfor',user)
    print('-')

    NSOVersion = Nxapi.GetNSOConfig()
    print(NSOVersion)
    print('-')
    nxapiToken=Nxapi.GetNxapiToken()
    print('nxapiToken:',nxapiToken)
    nxapiF=Nxapi.GetNxapiF(nxapiToken['access_token'],NSToken['id_token'],user['id'],user['language'],NSOVersion)
    print('nxapiF:',nxapiF)
    encryptedBody=base64.b64decode(nxapiF['encrypted_token_request'])
    print(encryptedBody)




if __name__ == '__main__':
    main()