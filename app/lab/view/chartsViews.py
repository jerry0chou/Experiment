from flask import request
from app.lab import lab
from app.lab.handle.handleCharts import handleGetExpCountByDate, handleGetExpDataResult, handleGetExpDetail


@lab.route('/getExpCountByDate', methods=['POST'])
def getExpCountByDate():
    uid = request.form.get('uid', None)
    return handleGetExpCountByDate(uid)


@lab.route('/getExpDataResult', methods=['POST'])
def getExpDataResult():
    uid = request.form.get('uid', None)
    return handleGetExpDataResult(uid)


@lab.route('/getExpDetail', methods=['POST'])
def getExpDetail():
    date = request.form.get('date', None)
    uid = request.form.get('uid', None)
    return handleGetExpDetail(date,uid)
