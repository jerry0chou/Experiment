from sqlalchemy import text
import datetime
from app.models import Experiment,Lab
from app import db
import json

def handleGetExperiments(page,per_page):
    status={0:"未进行",1:"正在进行",2:"已完成"}
    string="select experiment.eid,experiment.name as expname,lab.name as labname,experiment.date,experiment.status,account from experiment,lab,user where experiment.lid=lab.lid and experiment.uid=user.uid LIMIT "+str((page-1)*per_page)+" ,"+str(per_page)
    experiments=db.engine.execute(text(string))
    experimentList=[]
    for exp in experiments:
        ex={'eid':exp[0],'expname':exp[1],'labname':exp[2],'date':exp[3],'status':status[exp[4]],'account':exp[5]}
        experimentList.append(ex)

    res = db.engine.execute("select count(*) as count from experiment,lab,user where experiment.lid=lab.lid and experiment.uid=user.uid")
    count = [r[0] for r in res][0]

    labs = Lab.query.all()
    labJson = [r.to_json() for r in labs]

    users=db.engine.execute("select uid,account from user")
    userList=[]
    for row in users:
        user={'uid':row[0],'account':row[1]}
        userList.append(user)

    experimentInfo = {
        'experiments': experimentList,
        'count': count,
        'labs':labJson,
        'users':userList
    }
    return json.dumps(experimentInfo)

def handleSubmitExperimentEditForm(experiment):
    sql='update experiment set name='+"'"+ experiment['expname']+"'"+', date='+str(experiment['date'])
    if type(experiment['labname']) is int:
        sql=sql+", lid="+str(experiment['labname'])
    if len(experiment['status']) ==1:
        sql+=",status= "+str(experiment['status'])
    if type(experiment['account']) is int:
        sql+=",uid= "+str(experiment['account'])
    sql=sql+' where eid='+str(experiment['eid'])
    db.engine.execute(text(sql))
    return "success"

def handleSubmitExperimentAddForm(experiment):
    sql='INSERT INTO experiment (lid,uid,name,date,status) values (%d,%d,"%s",%d,%d)'%(experiment["labname"],experiment["account"],experiment["expname"],experiment["date"],int(experiment["status"]))
    db.engine.execute(text(sql))
    return "success"

def handleRemoveExperiment(eid):
    db.engine.execute('delete from experiment where eid='+str(eid))
    return "success"

def handleExperimentBatchDelete(eidList):
    for eid in eidList:
        db.engine.execute('delete from experiment where eid=' + str(eid))
    return "success"
