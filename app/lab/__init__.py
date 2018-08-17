from flask import Blueprint

lab=Blueprint('lab',__name__)

import app.lab.view.userViews
import app.lab.view.roleViews