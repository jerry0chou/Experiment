# coding:utf-8
from . import lab
from flask import render_template, request, Response
from .forms import handleLogin, handleGetUser, handleGetAllUser, handleRemoveUser, handleSummitUserEditForm, \
    handleSummitUserRegisterForm, handleQueryUser, handleBatchDelete
import json

@lab.route('/')
def index():
    return render_template("index.html")


@lab.route('/login', methods=['POST'])  #
def login():
    account = request.form.get('account', None)
    password = request.form.get('password', None)
    status = handleLogin(account, password)
    return Response(status)


@lab.route('/getUser', methods=['POST'])
def getUser():
    account = request.form.get('account', None)
    return handleGetUser(account)


@lab.route('/getAllUser', methods=['POST'])
def getAllUser():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)
    print("page", page, "per_page", per_page)
    print(type(page), type(per_page))
    if page and per_page:
        return handleGetAllUser(int(page), int(per_page))
    else:
        return "error"


@lab.route('/removeUser', methods=['POST'])
def removeUser():
    account = request.form.get('account', None)
    return handleRemoveUser(account)


# 修改用户
@lab.route('/summitUserEditForm', methods=['POST'])
def summitUserEditForm():
    account = request.form.get('account', None)
    username = request.form.get('username', None)
    phone = request.form.get('phone', None)
    roleName = request.form.get('roleName', None)
    password = request.form.get('password', None)
    return handleSummitUserEditForm(account, username, phone, roleName, password)


# 注册用户
@lab.route('/summitUserRegisterForm', methods=['POST'])
def summitUserRegisterForm():
    account = request.form.get('account', None)
    username = request.form.get('username', None)
    phone = request.form.get('phone', None)
    roleName = request.form.get('roleName', None)
    password = request.form.get('password', None)
    return handleSummitUserRegisterForm(account, username, phone, roleName, password)


@lab.route('/queryUser', methods=['POST'])
def queryUser():
    account = request.form.get('account', None)
    return handleQueryUser(account)


# 批量删除
@lab.route('/batchDelete', methods=['POST'])
def batchDelete():
    accountList = json.loads(request.form.get('accountList', None))
    print(accountList)
    return handleBatchDelete(accountList)
