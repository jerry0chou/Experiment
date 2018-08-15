from app import db
from app.models import User, Role
from werkzeug.security import check_password_hash
from flask import jsonify
import json


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


def handleGetAllUser(page,per_page):
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
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
        "pages": users.pages,
        "prev_num": users.prev_num,
        "has_prev": users.has_prev,
        "next_num": users.next_num,
        "has_next": users.has_next,
        "next_num": users.next_num
    }
    print("pageInfo",pageInfo)
    return json.dumps(pageInfo)

    # print(type(users))
    # print(users.items)
    # print(users.pages)
    # print(users.prev_num)
    # print(users.has_prev)
    # print(users.next_num)
    # print(users.next())  # 对象
    # print(users.has_next)
    # print(users.next_num)
    # print(type(users.next_num))

    # return json.dumps(userJson)
