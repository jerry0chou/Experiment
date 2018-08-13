# coding:utf-8
from . import lab

from flask import render_template,request,Response
from .forms import handleLogin

@lab.route('/')
def index():
    return render_template("index.html")


@lab.route('/login',methods=['POST']) #
def login():
    account=request.form.get('account',None)
    password = request.form.get('password',None)
    status=handleLogin(account,password)
    return Response(status)