# coding:utf-8
from . import lab

from flask import  render_template
@lab.route('/')
def index():
    return render_template("index.html")
