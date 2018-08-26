from functools import reduce
#from itertools import groupby
import json
import time,calendar

from sqlalchemy import text

from app import db
def handleGetExpCountByDate(uid):
    #print("getExpCountByDate uid", uid)
    expCount=db.engine.execute('select date from experiment where uid='+uid)

    def timestamp_datetime(value):
        format = '%Y-%m'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt



    #expList=[]
    # for exp in expCount:
    #     YM=exp[0].split(' ')[0].split('-')[0:-1]
    #     expList.append(reduce(lambda x,y:x+y,YM))
    expList=[]
    for e in expCount:
        expList.append(timestamp_datetime(e[0]//1000))

    #print(expList)
    expDict={}
    for exp in expList:
        if exp in expDict:
            value=expDict.get(exp)
            value=value+1
            expDict[exp]=value
        else:
            expDict[exp]=1
    #print(expDict)
    expInfoList=[]
    for key in expDict:
        tmp={}
        tmp['日期']=key
        tmp['实验次数']=expDict[key]
        expInfoList.append(tmp)
    #print(expInfoList)
    return json.dumps(expInfoList)
    #return "success"
def handleGetExpDataResult(uid):

    res=db.engine.execute('select encapsulation,discharge,charge,eficiency,loopretention,retention from expdata,experiment where expdata.eid=experiment.eid and experiment.uid='+uid)

    ExpDataResultList=[]
    for r in res:
        tmp={}
        tmp['包覆含量(%)']=r[0]
        tmp['1C首圈放电比容量(mAh/g)']=r[1]
        tmp['1C首圈充电比容量(mAh/g)']=r[2]
        tmp['首圈效率(%)']=r[3]
        tmp['1C循环50圈后放电容量']=r[4]
        tmp['容量保持率(%)']=r[5]
        ExpDataResultList.append(tmp)
    #print(ExpDataResultList)
    return json.dumps(ExpDataResultList)

def handleGetExpDetail(date,uid):
    print(date)
    dateSplit=date.split('-')
    print(dateSplit)
    monthRange = calendar.monthrange(int(dateSplit[0]),int(dateSplit[1]))
    print(monthRange[1])

    def datetime_timestamp(dt):
        time.strptime(dt, '%Y-%m-%d')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
        return int(s)*1000

    start=datetime_timestamp(date+"-01")
    end=datetime_timestamp(date+"-"+str(monthRange[1]))
    print(start,end)
    sql="""
    select encapsulation,discharge,charge,eficiency,loopretention,retention from expdata,experiment 
    where expdata.eid=experiment.eid and experiment.uid=%d and  date between %d and %d
    """%(int(uid),start,end)

    print(sql)
    res=db.engine.execute(text(sql))
    ExpDataResultList = []
    for r in res:
        tmp = {}
        tmp['包覆含量(%)'] = r[0]
        tmp['1C首圈放电比容量(mAh/g)'] = r[1]
        tmp['1C首圈充电比容量(mAh/g)'] = r[2]
        tmp['首圈效率(%)'] = r[3]
        tmp['1C循环50圈后放电容量'] = r[4]
        tmp['容量保持率(%)'] = r[5]
        ExpDataResultList.append(tmp)
    # print(ExpDataResultList)
    return json.dumps(ExpDataResultList)