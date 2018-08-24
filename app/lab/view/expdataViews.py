from werkzeug.utils import secure_filename

from app.lab import lab
from flask import request, send_file
from app import APP_STATIC_DOWNLOAD, APP_STATIC_UPLOAD
from app.lab.handle.handleExpData import handleGetExpDatas, handleSubmitExpDataEditForm, handleSubmitExpDataAddForm, \
    handleRemoveExpData, handleExpdataBatchDelete, handleExpdataQueryContent, handleDownExpData, handleUploadExpData
import json, os


@lab.route('/getExpDatas', methods=['POST'])
def getExpDatas():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)

    if page and per_page:
        return handleGetExpDatas(int(page), int(per_page))
    else:
        return "error"


@lab.route('/submitExpDataEditForm', methods=['POST'])
def submitExpDataEditForm():
    expdata = json.loads(request.form.get('expdata', None))
    return handleSubmitExpDataEditForm(expdata)


@lab.route('/submitExpDataAddForm', methods=['POST'])
def submitExpDataAddForm():
    expdata = json.loads(request.form.get('expdata', None))
    return handleSubmitExpDataAddForm(expdata)


@lab.route('/removeExpData', methods=['POST'])
def removeExpData():
    did = request.form.get('did', None)
    return handleRemoveExpData(did)


@lab.route('/expdataBatchDelete', methods=['POST'])
def expdataBatchDelete():
    didList = json.loads(request.form.get('didList', None))
    return handleExpdataBatchDelete(didList)


@lab.route('/expdataQueryContent', methods=['POST'])
def expdataQueryContent():
    selectType = request.form.get('selectType', None)
    content = request.form.get('content', None)
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)
    return handleExpdataQueryContent(selectType, content, page, per_page)


@lab.route('/downExpData', methods=['POST'])
def downExpData():
    userType = request.form.get('userType', None)

    if handleDownExpData(userType) == 'success':
        path = os.path.join(APP_STATIC_DOWNLOAD, 'expdata.xlsx')
        rv = send_file(path, attachment_filename=path, as_attachment=True)
        return rv
    else:
        return 'failure'


@lab.route('/uploadExpData', methods=['POST'])
def uploadExpData():
    file = request.files['file']
    uid=request.form.get('uid',None)
    print('uploadExpData uid:',uid)
    string = ''
    string.endswith(('.xls', '.xlsx'))
    if file.filename.endswith(('.xls', '.xlsx')):
        print(file.filename)
        path = os.path.join(APP_STATIC_UPLOAD, file.filename)
        file.save(path)
        handleUploadExpData(path,uid)

        return "success"
    else:
        return "failure"
