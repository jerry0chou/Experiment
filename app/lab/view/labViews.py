from app.lab import lab
from flask import  request, Response
from app.lab.handle.handleLab import handleGetLabs,handleEditLabName,handleAddLab

@lab.route('/getLabs')
def getLabs():
    return handleGetLabs()

@lab.route('/editLabName', methods=['POST'])
def editLabName():
    lid=request.form.get("lid",None)
    editLabName=request.form.get("editLabName",None)
    return handleEditLabName(lid,editLabName)

@lab.route('/addLab', methods=['POST'])
def addLab():
    labName=request.form.get("labName",None)
    return handleAddLab(labName)