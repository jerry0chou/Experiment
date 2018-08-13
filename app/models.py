from datetime import datetime
from app import db

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.debug = True
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/labpro.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)


# 角色
class Role(db.Model):
    __tablename__ = "role"
    rid = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    note = db.Column(db.String(100), default="")  # 备注
    # 关系
    users=db.relationship("User",backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

# 用户
class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    rid = db.Column(db.Integer, db.ForeignKey("role.rid"))  # 角色编号
    account = db.Column(db.String(50), unique=True)  # 账号
    username = db.Column(db.String(100), unique=True)  # 昵称
    password = db.Column(db.String(20))  # 密码
    phone = db.Column(db.Integer)  # 手机号码
    # 关系
    experiments = db.relationship("Experiment", backref="user")
    def __repr__(self):
        return '<User %r>' % self.username


# 仪器
class Appliance(db.Model):
    __tablename__ = "appliance"
    aid = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 仪器编号
    name = db.Column(db.String(50))  # 仪器名称
    manufacturer = db.Column(db.String(50))  # 生产厂家
    category = db.Column(db.String(50))  # 仪器型号
    note = db.Column(db.String(100), default="")  # 备注

    def __repr__(self):
        return '<appliance %r>' % self.name


# 材料
class Material(db.Model):
    __tablename__ = "material"
    mid = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 材料编号
    name = db.Column(db.String(50))  # 材料名称
    manufacturer = db.Column(db.String(50))  # 生产厂家
    purity = db.Column(db.String(50))  # 材料纯度
    note = db.Column(db.String(100), default="")  # 备注

    def __repr__(self):
        return '<material %r>' % self.name


# 实验室
class Lab(db.Model):
    __tablename__ = "lab"
    lid = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 实验室编号
    name = db.Column(db.String(50),unique=True)  # 实验室名称
    note = db.Column(db.String(100), default="")  # 备注
    # 关系
    experiments=db.relationship("Experiment",backref="lab")
    def __repr__(self):
        return '<lab %r>' % self.name


# 实验
class Experiment(db.Model):
    __tablename__ = "experiment"
    eid = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 实验编号
    lid = db.Column(db.Integer,db.ForeignKey("lab.lid"))  # 实验室编号
    uid = db.Column(db.Integer,db.ForeignKey("user.uid"))  # 用户编号
    name = db.Column(db.String(50))  # 实验名称
    data = db.Column(db.DateTime, index=True, default=datetime.now)
    status = db.Column(db.Integer)  # 状态0未进行,1正在进行,2已进行
    # 关系
    expdatas = db.relationship("ExpData", backref="experiment")
    def __repr__(self):
        return '<experiment %r>' % self.name


# 实验数据
class ExpData(db.Model):
    __tablename__ = "expdata"
    did = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 实验数据编号
    eid = db.Column(db.Integer,db.ForeignKey("experiment.eid"))  # 实验室编号
    encapsulation = db.Column(db.Float)  # 包覆含量
    discharge = db.Column(db.Float)  # 放电比容量
    charge = db.Column(db.Float)  # 充电比容量
    eficiency = db.Column(db.Float)  # 首圈效率
    loopretention = db.Column(db.Float)  # 循环50圈放电容量
    retention = db.Column(db.Float)  # 容量保持率

    def __repr__(self):
        return '<expdata %d>' % self.did


if __name__ == "__main__":
    # 创建 所有数据表
    """
    db.create_all()
    """
    print("testRole")
    # 测试插入数据
    """
    role=Role(
    name="教师",
    )
    
    db.session.add(role)
    db.session.commit()
    """

    # 测试插入admin 并且生成哈希密码
    """
    from werkzeug.security import generate_password_hash
    user=User(
        name="jane",
        pwd=generate_password_hash("123"),
        is_super=0,
        role_id=1
    )
    db.session.add(user)
    db.session.commit()
    """
    # role=Role.query.filter_by(name="教师").first()
    # print(role)
    # user = User.query.filter_by(username="jerry").first()
    # print(user)
# cd 到 app 命令行运行 python models.py
