from app.lab import lab
from flask import request, send_file
from app import APP_STATIC_DOWNLOAD
from app.lab.handle.handleExperiment import handleGetExperiments, handleSubmitExperimentEditForm, \
    handleSubmitExperimentAddForm, handleRemoveExperiment, handleExperimentBatchDelete, handleExperimentQueryContent, \
    handleDownExperiment
import json
import os


@lab.route('/getExperiments', methods=['POST'])
def getExperiment():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)

    if page and per_page:
        return handleGetExperiments(int(page), int(per_page))
    else:
        return "error"


@lab.route('/submitExperimentEditForm', methods=['POST'])
def submitExperimentEditForm():
    experiment = json.loads(request.form.get('experiment', None))
    return handleSubmitExperimentEditForm(experiment)


@lab.route('/submitExperimentAddForm', methods=['POST'])
def submitExperimentAddForm():
    experiment = json.loads(request.form.get('experiment', None))
    return handleSubmitExperimentAddForm(experiment)


@lab.route('/removeExperiment', methods=['POST'])
def removeExperiment():
    eid = request.form.get('eid', None)
    return handleRemoveExperiment(eid)


# experimentBatchDelete

@lab.route('/experimentBatchDelete', methods=['POST'])
def experimentBatchDelete():
    eidList = json.loads(request.form.get('eidList', None))
    return handleExperimentBatchDelete(eidList)


@lab.route('/experimentQueryContent', methods=['POST'])
def experimentQueryContent():
    selectType = request.form.get('selectType', None)
    statusType = request.form.get('statusType', None)
    content = request.form.get('content', None)
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)
    return handleExperimentQueryContent(selectType, statusType, content, int(page), int(per_page))


@lab.route('/downExperiment', methods=['POST'])
def downExperiment():
    downloadExpStatus = request.form.get('downloadExpStatus', None)

    if handleDownExperiment(downloadExpStatus) == 'success':
        path = os.path.join(APP_STATIC_DOWNLOAD, 'experiment.xlsx')
        print(path)
        rv=send_file(path,attachment_filename=path,as_attachment=True)
        return rv
    else:
        return 'failure'
