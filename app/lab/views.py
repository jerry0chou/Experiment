# coding:utf-8
from . import lab

from flask import render_template, request, Response
from .forms import handleLogin,handleGetUser,handleGetAllUser


@lab.route('/')
def index():
    return render_template("index.html")


@lab.route('/login', methods=['POST'])  #
def login():
    account = request.form.get('account', None)
    password = request.form.get('password', None)
    status = handleLogin(account, password)
    return Response(status)


@lab.route('/getUser',methods=['POST'])
def getUser():
    account = request.form.get('account', None)
    return handleGetUser(account)

@lab.route('/getAllUser',methods=['POST'])
def getAllUser():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)
    print("page",page,"per_page",per_page)
    print(type(page),type(per_page))
    if page and per_page:
        return handleGetAllUser(int(page),int(per_page))
    else:
        return "error"
