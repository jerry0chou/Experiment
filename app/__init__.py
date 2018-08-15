# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import pymysql

app=Flask(__name__)
app.debug=True

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/labpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# 蓝图注册
from app.lab import lab as lab_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(lab_blueprint)
app.register_blueprint(admin_blueprint,url_prefix='/admin')