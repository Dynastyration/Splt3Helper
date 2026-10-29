import Http

SPLATNET3_URL='https://api.lp1.av5ja.srv.nintendo.net'
WEB_VIEW_VER='10.0.0-88706e32'
APP_USER_AGENT_TEMPLATE='com.nintendo.znca/{}(Android/14)'

QUERY_HASH={
    'LatestBattleHistoriesQuery':'b24d22fd6cb251c515c2b90044039698aa27bc1fab15801d83014d919cd45780',
    'RegularBattleHistoriesQuery':'2fe6ea7a2de1d6a888b7bd3dbeb6acc8e3246f055ca39b80c4531bbcd0727bba',
    'BankaraBattleHistoriesQuery':'9863ea4744730743268e2940396e21b891104ed40e2286789f05100b45a0b0fd',
    'XBattleHistoriesQuery':'eb5996a12705c2e94813a62e05c0dc419aad2811b8d49d53e5732290105559cb',
    'VsHistoryDetailQuery':'94faa2ff992222d11ced55e0f349920a82ac50f414ae33c83d1d1c9d8161c5dd',
    'CoopHistoryQuery':'e11a8cf2c3de7348495dea5cdcaa25e0c153541c4ed63f044b6c174bc5b703df',
    'CoopHistoryDetailQuery':'f2d55873a9281213ae27edc171e2b19131b3021a2ae263757543cdd3bf015cc8',
}

def QueryGraphQL(gtoken:str,bulletToken:str,NSOVersion:str,language:str,country:str,queryName:str,variables:dict|None=None)->dict:
    header={
        'Authorization':    f'Bearer {bulletToken}',
        'Accept-Language':  language,
        'User-Agent':       APP_USER_AGENT_TEMPLATE.format(NSOVersion),
        'X-Web-View-Ver':   WEB_VIEW_VER,
        'Content-Type':     'application/json',
        'Accept':           '*/*',
        'Origin':           SPLATNET3_URL,
        'X-Requested-With': 'com.nintendo.znca',
        'Referer':          f'{SPLATNET3_URL}/?lang={language}&na_country={country}&na_lang={language}',
        'Accept-Encoding':  'gzip, deflate'}
    body={
        'extensions':{'persistedQuery':{'sha256Hash':QUERY_HASH[queryName],'version':1}},
        'variables':variables or {}}
    resp=Http.httpSession.post(SPLATNET3_URL+'/api/graphql',
                               headers=header,json=body,
                               cookies={'_gtoken':gtoken,'_dnt':'1'},
                               timeout=(30,120))
    return resp.json()
