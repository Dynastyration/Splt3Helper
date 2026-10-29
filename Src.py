import Session
import Nxapi
import base64
import SplatNet
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
    nxapiF=Nxapi.GetNxapiF1(nxapiToken['access_token'],NSToken['id_token'],user['id'],user['language'],NSOVersion)
    print('nxapiF:',nxapiF)
    encryptedBody=base64.b64decode(nxapiF['encrypted_token_request'])
    print(encryptedBody)
    nsocoral=Nxapi.GetNSOCoralToken(encryptedBody,nxapiToken['access_token'],NSOVersion)
    print(nsocoral)
    coralToken=nsocoral['result']['webApiServerCredential']['accessToken']
    coralUserId=nsocoral['result']['user']['id']

    nxapif2=Nxapi.GetNxapiF2(nxapiToken['access_token'],coralToken,user['id'],coralUserId,NSOVersion)
    print('nxapif2:',nxapif2)
    webService=Nxapi.GetWebServiceToken(base64.b64decode(nxapif2['encrypted_token_request']),
                                        nxapiToken['access_token'],coralToken,NSOVersion)
    print('webService:',webService)
    gtoken=webService['result']['accessToken']
    print('gtoken:',gtoken)

    bulletToken=Nxapi.GetBulletToken(gtoken,NSOVersion,user['language'],user['country'])
    print('bulletToken:',bulletToken)
    battle=SplatNet.QueryGraphQL(gtoken,bulletToken,NSOVersion,user['language'],user['country'],
                                'LatestBattleHistoriesQuery')
    print(battle)



if __name__ == '__main__':
    main()