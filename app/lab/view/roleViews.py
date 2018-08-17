
from app.lab import lab
from flask import  request, Response
from app.lab.handle.handleRole import handleGetAllRole,handleAddRole,handleEditRoleName
@lab.route('/getAllRole')
def getAllRole():
    return handleGetAllRole()

@lab.route('/addRole', methods=['POST'])
def addRole():
    roleName=request.form.get("roleName",None)
    print("roleName:",roleName)
    return handleAddRole(roleName)

@lab.route('/editRoleName', methods=['POST'])
def editRoleName():
    rid=request.form.get("rid",None)
    editRoleName=request.form.get("editRoleName",None)
    print("editRoleName:",editRoleName)
    print("rid:",rid)
    return handleEditRoleName(rid,editRoleName)