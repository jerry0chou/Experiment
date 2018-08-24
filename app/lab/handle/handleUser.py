from sqlalchemy import text

from app import db
from app.models import User, Role
from werkzeug.security import check_password_hash
import json

from werkzeug.security import generate_password_hash




def handleLogin(account, password):
    user = User.query.filter_by(account=account).first()
    status=''
    userJson={}
    if user is None or check_password_hash(user.password, password) == False:
         status="failure"
    else:
        role = Role.query.get(user.rid)
        userJson=user.to_json()
        userJson["roleName"] = role.name
        status = "success"

    userInfo={
        'status':status,
        'user':userJson
    }
    return json.dumps(userInfo)

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
    return json.dumps(pageInfo)


def handleRemoveUser(account):
    sql="""
    select user.uid from user where user.uid in (select experiment.uid from experiment) and account='%s'
    """%(account)
    res = db.engine.execute(text(sql))
    exist = [r[0] for r in res]
    if len(exist) == 0:
        db.engine.execute("delete from user where account='%s'"%(account))
        return "success"
    else:
        return "该用户已经做了实验,不能删除"


def handleSummitUserEditForm(account, username, phone, roleName, password):
    user = User.query.filter_by(account=account).first()
    role = Role.query.filter_by(name=roleName).first()
    if user:
        user.username = username
        if password != '':
            user.password = generate_password_hash(password)
        user.rid = role.rid
        user.phone = phone
        db.session.commit()
        return "success"
    else:
        return "failure"


def handleSummitUserRegisterForm(account, username, phone, roleName, password):
    user = User.query.filter_by(account=account).first()
    if user:
        return "账户已存在，不能注册"
    else:
        role = Role.query.filter_by(name=roleName).first()
        user = User(
            rid=role.rid,
            account=account,
            username=username,
            password=generate_password_hash(password),
            phone=phone
        )
        db.session.add(user)
        db.session.commit()
        return "success"


def handleQueryUser(account):
    user = User.query.filter_by(account=account).first()
    roles = Role.query.all()
    roleJson = [r.to_json() for r in roles]
    users = []
    if user:
        userJson = user.to_json()
        for role in roleJson:
            if role["rid"] == user.rid:
                userJson["roleName"] = role['name']
        users.append(userJson)
        return json.dumps(users)
    else:
        return "failure"


def handleBatchDelete(accountList):
    for account in accountList:
        handleRemoveUser(account)
    return "success"
