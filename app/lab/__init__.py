from flask import Blueprint

lab=Blueprint('lab',__name__)

import app.lab.view.userViews
import app.lab.view.roleViews
import app.lab.view.applianceViews
import app.lab.view.materialViews
import app.lab.view.labViews
import app.lab.view.experimentViews
import app.lab.view.expdataViews
import app.lab.view.chartsViews