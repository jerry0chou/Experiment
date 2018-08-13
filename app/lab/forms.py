from app import db
from app.models import User


def handleLogin(account, password):
    user = User.query.filter_by(account=account).first()
    if user is None or user.password!=password:
        return "failure"
    else:
        return "success"


