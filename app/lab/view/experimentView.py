from app.lab import lab
from flask import  request
from app.lab.handle.handleExperiment import handleGetExperiments,handleSubmitExperimentEditForm,handleSubmitExperimentAddForm,handleRemoveExperiment,handleExperimentBatchDelete
import json
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