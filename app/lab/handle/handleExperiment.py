from sqlalchemy import text
import datetime
from app.models import Experiment, Lab
from app import db
import json
import pandas as pd
import os
import time
from app import APP_STATIC_DOWNLOAD

status = {0: "未进行", 1: "正在进行", 2: "已完成"}

def makeExperimentInfo(expSql, countSql):
    experiments = db.engine.execute(text(expSql))
    expList = []
    for exp in experiments:
        ex = {'eid': exp[0], 'expname': exp[1], 'labname': exp[2], 'date': exp[3], 'status': status[exp[4]],
              'account': exp[5]}
        expList.append(ex)

    res = db.engine.execute(text(countSql))
    count = [r[0] for r in res][0]
    return expList, count


def handleGetExperiments(page, per_page):

    expSql = "select experiment.eid,experiment.name as expname,lab.name as labname,experiment.date,experiment.status,account from experiment,lab,user where experiment.lid=lab.lid and experiment.uid=user.uid LIMIT " + str(
        (page - 1) * per_page) + " ," + str(per_page)

    countSql='select count(*) as count from experiment,lab,user where experiment.lid=lab.lid and experiment.uid=user.uid'
    experimentList,count=makeExperimentInfo(expSql,countSql)

    labs = Lab.query.all()
    labJson = [r.to_json() for r in labs]

    users = db.engine.execute("select uid,account from user")
    userList = []
    for row in users:
        user = {'uid': row[0], 'account': row[1]}
        userList.append(user)

    experimentInfo = {
        'experiments': experimentList,
        'count': count,
        'labs': labJson,
        'users': userList
    }
    return json.dumps(experimentInfo)


def handleSubmitExperimentEditForm(experiment):
    sql = 'update experiment set name=' + "'" + experiment['expname'] + "'" + ', date=' + str(experiment['date'])
    if type(experiment['labname']) is int:
        sql = sql + ", lid=" + str(experiment['labname'])
    if len(experiment['status']) == 1:
        sql += ",status= " + str(experiment['status'])
    if type(experiment['account']) is int:
        sql += ",uid= " + str(experiment['account'])
    sql = sql + ' where eid=' + str(experiment['eid'])
    db.engine.execute(text(sql))
    return "success"


def handleSubmitExperimentAddForm(experiment):
    sql = 'INSERT INTO experiment (lid,uid,name,date,status) values (%d,%d,"%s",%d,%d)' % (
    experiment["labname"], experiment["account"], experiment["expname"], experiment["date"], int(experiment["status"]))
    db.engine.execute(text(sql))
    return "success"


def handleRemoveExperiment(eid):
    res=db.engine.execute("select experiment.eid from experiment where experiment.eid in (select expdata.eid from expdata) and experiment.eid="+str(eid))
    exist = [r[0] for r in res]
    if len(exist)==0:
        db.engine.execute('delete from experiment where eid=' + str(eid))
        return "success"
    else:
        return "实验已经产生数据,不能删除"


def handleExperimentBatchDelete(eidList):
    for eid in eidList:
        handleRemoveExperiment(eid)
    return "success"


def handleExperimentQueryContent(selectType, statusType, content, page, per_page):
    limitSql=" LIMIT " + str((page - 1) * per_page) + " ," + str(per_page)
    commonExpSql="""
    select experiment.eid,experiment.name as expname,lab.name as labname,experiment.date,
        experiment.status,account from experiment,lab,user where experiment.lid=lab.lid 
        and experiment.uid=user.uid and
    """
    commonCountSQl="""
    select count() as count from experiment,lab,user where experiment.lid=lab.lid 
        and experiment.uid=user.uid and 
    """
    experimentList=[]
    count=0
    if content == '' and statusType != '-1':
        expSql=commonExpSql+" status="+statusType+limitSql
        countSql=commonCountSQl+" status="+statusType
        experimentList,count=makeExperimentInfo(expSql,countSql)


    elif content != '' and statusType == '-1':
        if selectType =='eid':
            expSql=commonExpSql+" experiment.eid="+content
            countSql=commonCountSQl+" experiment.eid="+content
            experimentList, count = makeExperimentInfo(expSql, countSql)

        elif selectType=='expname':
            expSql = commonExpSql + " expname like " +"'%"+ content+"%'"+limitSql
            countSql = commonCountSQl + " experiment.name like " +"'%"+ content+"%'"
            experimentList, count = makeExperimentInfo(expSql, countSql)
        elif selectType=='account':
            expSql = commonExpSql + " account= "+"'"+ content+ "'"+limitSql
            countSql = commonCountSQl + " account= "+ "'"+content+"'"
            experimentList, count = makeExperimentInfo(expSql, countSql)

    elif content != '' and statusType != '-1':
        if selectType =='eid':
            expSql=commonExpSql+" experiment.eid="+content+" and status="+statusType
            countSql=commonCountSQl+" experiment.eid="+content+" and status="+statusType
            experimentList, count = makeExperimentInfo(expSql, countSql)

        elif selectType=='expname':
            expSql = commonExpSql + " expname like " +"'%"+ content+"%'"+" and status="+statusType + limitSql
            countSql = commonCountSQl + " experiment.name like " +"'%"+ content+"%'"+" and status="+statusType
            experimentList, count = makeExperimentInfo(expSql, countSql)
        elif selectType=='account':
            expSql = commonExpSql + " account= "+"'"+ content+ "'"+" and status="+statusType +limitSql
            countSql = commonCountSQl + " account= "+ "'"+content+"'"+" and status="+statusType
            experimentList, count = makeExperimentInfo(expSql, countSql)

    experimentInfo = {
        'experiments': experimentList,
        'count': count
    }
    return json.dumps(experimentInfo)


def handleDownExperiment(downloadExpStatus):
    commonSql="""
    select experiment.eid,experiment.name as expname,lab.name as labname,experiment.date,
        experiment.status,account from experiment,lab,user where experiment.lid=lab.lid
        and experiment.uid=user.uid 
    """
    expSql=''
    if downloadExpStatus =='-1':
        expSql=commonSql
    else:
        expSql=commonSql+" and experiment.status="+downloadExpStatus

    expList=pd.read_sql_query(expSql,db.engine)

    def timestamp_datetime(value):
        format = '%Y-%m-%d'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt

    expList.columns=['实验编号', '实验名称', '实验地点','实验时间','实验状态','用户账号']
    expList['实验状态'].replace({0:"未进行",1:"正在进行",2:"已完成"},inplace=True)
    expList['实验时间'] = expList['实验时间'] // 1000
    expList['实验时间'] = expList['实验时间'].apply(timestamp_datetime)
    path = os.path.join(APP_STATIC_DOWNLOAD, 'experiment.xlsx')
    expList.to_excel(path,index=False)
    return  "success"