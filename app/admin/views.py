# coding:utf-8
from . import admin

from flask import jsonify,request,Response

@admin.route('/')
def index():
    return "<h1 style='color:red'>this this admin</h1>"

@admin.route('/add')
def addRole():

    return "addRole"