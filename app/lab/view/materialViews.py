from app.lab import lab
from flask import render_template, request, Response
from app.lab.handle.handleMaterial import handleGetMaterials,handleSubmitMaterialEditForm,HnadleSubmitMaterialAddForm,handleRemoveMaterial,handleMaterialBatchDelete,handleMaterialQueryContent
import json
@lab.route('/getMaterials', methods=['POST'])
def getMaterials():
    page = request.form.get('page', None)
    per_page = request.form.get('per_page', None)

    if page and per_page:
        return handleGetMaterials(int(page), int(per_page))
    else:
        return "error"

@lab.route('/submitMaterialEditForm', methods=['POST'])
def summitMaterialEditForm():
    material = json.loads(request.form.get('material', None))
    return handleSubmitMaterialEditForm(material)


@lab.route('/submitMaterialAddForm', methods=['POST'])
def submitMaterialAddForm():
    material = json.loads(request.form.get('material', None))
    return HnadleSubmitMaterialAddForm(material)

@lab.route('/removeMaterial', methods=['POST'])
def removeMaterial():
    mid = request.form.get('mid', None)
    return handleRemoveMaterial(mid)

@lab.route('/materialBatchDelete', methods=['POST'])
def materialBatchDelete():
    midList = json.loads(request.form.get('midList', None))
    return handleMaterialBatchDelete(midList)

@lab.route('/materialQueryContent', methods=['POST'])
def materialQueryContent():
    selectType = request.form.get('selectType', None)
    content=request.form.get('content', None)
    page=request.form.get('page', None)
    per_page=request.form.get('per_page', None)
    return handleMaterialQueryContent(selectType,content,page,per_page)