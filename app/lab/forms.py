from app import db
from app.models import User, Role
from werkzeug.security import check_password_hash
from flask import jsonify
import json

from werkzeug.security import generate_password_hash


def handleLogin(account, password):
    user = User.query.filter_by(account=account).first()
    if user is None or check_password_hash(user.password, password) == False:
        return "failure"
    else:
        return "success"


def handleGetUser(account):
    user = User.query.filter_by(account=account).first()
    role = Role.query.get(user.rid)
    userJson = user.to_json()
    userJson["roleName"] = role.name
    return json.dumps(userJson)


def handleGetAllUser(page, per_page):
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    res = db.engine.execute("select count(*) from user")
    count = [r[0] for r in res][0]
    roles = Role.query.all()
    roleJson = [r.to_json() for r in roles]
    userList = []

    def makeUsers(items):
        for user in items:
            userJson = user.to_json()
            for r in roleJson:
                if userJson['rid'] == r['rid']:
                    userJson["roleName"] = r['name']
                    userList.append(userJson)

    makeUsers(users.items)
    pageInfo = {
        "users": userList,
        "count": count,
        "roleList": roleJson
    }
    print("pageInfo", pageInfo)
    return json.dumps(pageInfo)


def handleRemoveUser(account):
    user = User.query.filter_by(account=account).first()
    print(user)
    if user:
        print(user.account)
        db.session.delete(user)
        db.session.commit()
        return "success"
    else:
        return "failure"


def handleSummitUserEditForm(account, username, phone, roleName, password):
    user = User.query.filter_by(account=account).first()
    role = Role.query.filter_by(name=roleName).first()

    print("roleName:",len(roleName),"role",role.rid,role.name)
    print("summitUser",account, username, phone, password, roleName)

    if user :
        user.username=username
        user.password=generate_password_hash(password)
        user.rid=role.rid
        user.phone=phone
        db.session.commit()
        return "success"
    else:
        return "failure"
