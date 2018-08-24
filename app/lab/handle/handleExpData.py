from sqlalchemy import text
from app.models import ExpData,Experiment
from app import db,APP_STATIC_DOWNLOAD
import json,time,os
import pandas as pd
import datetime
from app.lab.handle.handleLab import handleGetLid

def handleGetExpDatas(page, per_page):
    res = db.engine.execute("select count(*) as count from expdata")
    count = [r[0] for r in res][0]

    sql = "select expdata.did, expdata.eid,experiment.name,encapsulation,discharge,charge,eficiency,loopretention,retention from expdata,experiment where expdata.eid=experiment.eid  LIMIT " + str(
        (page - 1) * per_page) + " ," + str(per_page)
    expdataTu = db.engine.execute(text(sql))

    expdataList = []
    for expdata in expdataTu:
        exp = {'did': expdata[0], 'eid': expdata[1], 'expname': expdata[2], 'encapsulation': expdata[3],
               'discharge': expdata[4], 'charge': expdata[5], 'eficiency': expdata[6], 'loopretention': expdata[7],
               'retention': expdata[8]}
        expdataList.append(exp)

    expdataSql='select experiment.eid ,experiment.name from experiment where experiment.eid not in (select expdata.eid from expdata)'
    expTu=db.engine.execute(text(expdataSql))
    availableExpList=[]
    for exper in expTu:
        ex={'eid':exper[0],'expname':exper[1]}
        availableExpList.append(ex)

    expdataInfo = {
        'expdatas': expdataList,
        'count': count,
        'availableExp':availableExpList
    }
    return json.dumps(expdataInfo)

def handleSubmitExpDataEditForm(expdata):
    exp = ExpData.query.filter_by(did=expdata['did']).first()
    if exp:
        exp.encapsulation = expdata['encapsulation']
        exp.discharge = expdata['discharge']
        exp.charge = expdata['charge']
        exp.eficiency = expdata['eficiency']
        exp.loopretention = expdata['loopretention']
        exp.retention = expdata['retention']
        db.session.commit()
        return "success"
    else:
        return "failure"
    return "success"

def handleSubmitExpDataAddForm(expdata):
    sql = 'INSERT INTO expdata (eid,encapsulation,discharge,charge,eficiency,loopretention,retention) values (%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f)'%(
        expdata["availExp"], expdata["encapsulation"],
        expdata["discharge"], expdata["charge"], expdata['eficiency'],expdata['loopretention'],expdata['retention'])
    db.engine.execute(text(sql))
    return "success"

def handleRemoveExpData(did):
    db.engine.execute('delete from expdata where did='+str(did))
    return "success"

def handleExpdataBatchDelete(didList):
    for did in didList:
        db.engine.execute('delete from expdata where did=' + str(did))
    return "success"

def handleExpdataQueryContent(selectType,content,page,per_page):
    countexpnameSql="""
    select count(did) as count from expdata,experiment where expdata.eid=experiment.eid and experiment.name like 
    """
    expnameSql = """
        select  expdata.did, expdata.eid,experiment.name as expname,
        encapsulation,discharge,charge,eficiency,loopretention,retention 
        from expdata,experiment where expdata.eid=experiment.eid and expname like 
    """
    eidSql="""
    select  expdata.did, expdata.eid,experiment.name as expname,
    encapsulation,discharge,charge,eficiency,loopretention,retention
    from expdata,experiment where expdata.eid=experiment.eid and expdata.eid=
    """
    count=0
    expdataList=[]

    def makeExpdataList(sql):
        expdataTu = db.engine.execute(text(sql))
        for expdata in expdataTu:
            exp = {'did': expdata[0], 'eid': expdata[1], 'expname': expdata[2], 'encapsulation': expdata[3],
                   'discharge': expdata[4], 'charge': expdata[5], 'eficiency': expdata[6], 'loopretention': expdata[7],
                   'retention': expdata[8]}
            expdataList.append(exp)

    if selectType=='expname':
        common = "'%" + content + "%'"
        countexpnameSql += common
        expnameSql += common
        res = db.engine.execute(text(countexpnameSql))
        count = [r[0] for r in res][0]
        makeExpdataList(expnameSql)

    if selectType=='eid' and content.isdigit():
        count=1
        eidSql += str(content)
        makeExpdataList(eidSql)

    expdatasInfo = {
        'expdatas': expdataList,
        'count': count
    }
    return json.dumps(expdatasInfo)

def handleDownExpData(userType):
    commonSql = """
      select experiment.name as expname,experiment.date,lab.name as labname,encapsulation,discharge,charge,eficiency,loopretention,retention
      from experiment,lab,expdata where experiment.lid=lab.lid and expdata.eid=experiment.eid
    """
    expSql = ''
    if userType=='all':
        expSql=commonSql

    else:
        expSql=commonSql+' and experiment.uid='+userType

    expDataList = pd.read_sql_query(expSql, db.engine)

    def timestamp_datetime(value):
        format = '%Y-%m-%d'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt

    expDataList.columns = ['实验名称', '实验时间', '实验地点', '包覆含量(%)', '1C首圈放电比容量(mAh/g)', '1C首圈充电比容量(mAh/g)','首圈效率(%)','1C循环50圈后放电容量','容量保持率(%)']
    expDataList['实验时间'] = expDataList['实验时间'] // 1000
    expDataList['实验时间'] = expDataList['实验时间'].apply(timestamp_datetime)
    path = os.path.join(APP_STATIC_DOWNLOAD, 'expdata.xlsx')
    expDataList.to_excel(path,index=False)
    return "success"

def handleUploadExpData(path,uid):
    uploadExcel=pd.read_excel(path)
    print(uploadExcel.columns[0])
    if '条件变量' in uploadExcel.columns[0]:
        uploadExcel = pd.read_excel(path, header=None)
        uploadExcel = uploadExcel[2:-1]
        uploadExcel.columns = ['实验名称', '实验时间', '实验地点', '包覆含量（%）', '1C首圈放电比容量(mAh/g)', '1C首圈充电比容量(mAh/g)', '首圈效率(%)',
                               '1C循环50圈后放电容量', '容量保持率(%)']
        uploadExcel.reset_index(inplace=True, drop=True)

    uploadExcel['实验时间'] = pd.to_datetime(uploadExcel['实验时间'])


    # def datetime_timestamp(dt):
    #     time.strptime(dt, '%Y-%m-%d')
    #     s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
    #     return int(s)*1000



    #uploadExcel['实验时间'] = uploadExcel['实验时间'].astype('str').apply(datetime_timestamp)
    uploadExcel.columns = ['expname', 'date', 'labname', 'encapsulation', 'discharge', 'charge', 'eficiency',
                           'loopretention', 'retention']

    #print(uploadExcel.head())
    length=uploadExcel.shape[0]
    print("length",length)
    for row in range(length):
        excelRowJson=json.loads(uploadExcel.iloc[row].to_json(force_ascii=False))
        print(excelRowJson)
        if excelRowJson['expname'] == None:
            break
        labid=handleGetLid(excelRowJson['labname'])
        experiment=Experiment(
            lid=labid,
            uid=uid,
            name=excelRowJson['expname'],
            date=datetime.datetime.fromtimestamp(excelRowJson['date']//1000),
            status=2
        )
        db.session.add(experiment)
        db.session.commit()
        expdata=ExpData(
            eid=experiment.eid,
            encapsulation=excelRowJson['encapsulation'],
            discharge=excelRowJson['discharge'],
            charge=excelRowJson['charge'],
            eficiency=excelRowJson['eficiency'],
            loopretention=excelRowJson['loopretention'],
            retention=excelRowJson['loopretention']
        )
        db.session.add(expdata)
        db.session.commit()
