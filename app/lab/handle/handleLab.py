from app import db
from app.models import  Lab
import json

def handleGetLabs():
    labs = Lab.query.all()
    labJson = [r.to_json() for r in labs]
    return json.dumps(labJson)

def handleEditLabName(lid,editLabName):
    lab = Lab.query.filter_by(lid=lid).first()
    if lab:
        lab.name=editLabName
        db.session.commit()
        return "success"
    else:
        return "failure"

def handleAddLab(labName):
    lab = Lab.query.filter_by(name=labName).first()
    if lab:
        return "实验室名已经存在，请重新输入"
    else:
        lab = Lab(name=labName)
        db.session.add(lab)
        db.session.commit()
        return "success"

def handleGetLid(labName):
    lab = Lab.query.filter_by(name=labName).first()
    if lab:
        return lab.lid
    else:
        lab = Lab(name=labName)
        db.session.add(lab)
        db.session.commit()
        return lab.lid