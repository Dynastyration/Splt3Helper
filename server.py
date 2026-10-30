from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app=FastAPI(title='Splt3Helper')

@app.post('/api/session')
def CreateSession():
    EnsureSession()
    return {'nickname':state.user.get('nickname'),'language':state.language,
            'expiresAt':state.expiresAt.isoformat()}

@app.get('/api/session')
def ReadSession():
    if state.bulletToken is None:
        return {'loggedIn':False}
    remain=int((state.expiresAt-datetime.now()).total_seconds())
    return {'loggedIn':remain>0,'nickname':state.user.get('nickname'),'remainSeconds':max(remain,0)}

@app.delete('/api/session')
def DeleteSession():
    state.__init__()
    return {'loggedIn':False}

@app.get('/api/battles')
def ListBattles(mode:str=Query('latest',pattern='^(latest|regular|bankara|x|event)$'),
                limit:int=Query(50,ge=1,le=200)):
    EnsureSession()
    if mode=='event':
        raise HTTPException(400,'祭典对战接口还没接，先不要用 event')
    query=QUERY_NAME[mode]
    data=SplatNet.QueryGraphQL(state.gtoken,state.bulletToken,state.version,
                               state.language,state.country,query)
    rows=SplatNet.CollectBattles(data,ROOT_KEY[mode])
    for row in rows:
        row['time']=row['time'].isoformat() if row['time'] else None
    return {'total':len(rows),'items':rows[:limit]}

@app.get('/api/battles/stats')
def BattleStats(mode:str=Query('latest')):
    EnsureSession()
    data=SplatNet.QueryGraphQL(state.gtoken,state.bulletToken,state.version,
                               state.language,state.country,QUERY_NAME[mode])
    rows=SplatNet.CollectBattles(data,ROOT_KEY[mode])
    def bucket(key):
        result={}
        for row in rows:
            slot=result.setdefault(row[key],[0,0])
            slot[0]+=1
            slot[1]+=row['result']=='WIN'
        return {name:{'total':total,'wins':wins,'rate':round(wins/total,4)}
                for name,(total,wins) in result.items()}
    total=len(rows)
    wins=sum(1 for row in rows if row['result']=='WIN')
    return {'total':total,'wins':wins,'rate':round(wins/total,4) if total else 0,
            'byRule':bucket('rule'),'byStage':bucket('stage'),'byWeapon':bucket('weapon')}

@app.get('/api/battles/{battleId}')
def BattleDetail(battleId:str):
    EnsureSession()
    data=SplatNet.QueryGraphQL(state.gtoken,state.bulletToken,state.version,
                               state.language,state.country,'VsHistoryDetailQuery',
                               {'vsResultId':battleId})
    if 'errors' in data:
        raise HTTPException(404,'找不到这场战报')
    return data['data']['vsHistoryDetail']
