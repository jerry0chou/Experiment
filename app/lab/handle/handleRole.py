from app import db
from app.models import  Role
import json

def handleGetAllRole():
    roles = Role.query.all()
    roleJson = [r.to_json() for r in roles]
    return json.dumps(roleJson)

def handleAddRole(roleName):
    role = Role.query.filter_by(name=roleName).first()
    if role:
        return "角色名已经存在，请重新输入"
    else:
        r=Role(name=roleName)
        db.session.add(r)
        db.session.commit()
        return "success"

def handleEditRoleName(rid,editRoleName):
    role = Role.query.filter_by(rid=rid).first()
    if role:
        role.name=editRoleName
        db.session.commit()
        return "success"
    else:
        return "failure"