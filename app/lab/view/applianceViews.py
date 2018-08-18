from app.lab import lab
from flask import render_template, request, Response
from app.lab.handle.handleAppliance import handleGetAppliances,handleSummitApplianceEditForm,handleSummitApplianceAddForm,handleRemoveAppliance,handleApplianceBatchDelete,handleAppllianceQueryContent
import json
@lab.route('/getAppliances', methods=['POST'])
def getAppliances():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)

    if page and per_page:
        return handleGetAppliances(int(page), int(per_page))
    else:
        return "error"


@lab.route('/summitApplianceEditForm', methods=['POST'])
def summitApplianceEditForm():
    appliance = json.loads(request.form.get('appliance', None))
    return handleSummitApplianceEditForm(appliance)


@lab.route('/summitApplianceAddForm', methods=['POST'])
def summitApplianceAddForm():
    appliance = json.loads(request.form.get('appliance', None))
    #print("summitApplianceAddForm:",appliance)
    return handleSummitApplianceAddForm(appliance)

@lab.route('/removeAppliance', methods=['POST'])
def removeAppliance():
    aid = request.form.get('aid', None)
    print("aid：",aid)
    return handleRemoveAppliance(aid)

#applianceBatchDelete
# 批量删除
@lab.route('/applianceBatchDelete', methods=['POST'])
def applianceBatchDelete():
    aidList = json.loads(request.form.get('aidList', None))
    return handleApplianceBatchDelete(aidList)

# AppllianceQueryContenat
@lab.route('/appllianceQueryContent', methods=['POST'])
def appllianceQueryContent():
    selectType = request.form.get('selectType', None)
    content=request.form.get('content', None)
    page=request.form.get('page', None)
    per_page=request.form.get('per_page', None)
    print("selectType content page per_page",selectType,content,page,per_page)
    return handleAppllianceQueryContent(selectType,content,page,per_page)