from app.models import Material
from app import db
import json

def handleGetMaterials(page,per_page):
    materials = Material.query.paginate(page=page, per_page=per_page, error_out=False)
    res = db.engine.execute("select count(*) from material")
    count = [r[0] for r in res][0]
    materialInfo = {
        'materials': [a.to_json() for a in materials.items],
        'count': count
    }
    return json.dumps(materialInfo)

def handleSubmitMaterialEditForm(material):
    mater = Material.query.filter_by(mid=material['mid']).first()
    if mater:
        mater.name=material['name']
        mater.purity=material['purity']
        mater.manufacturer=material['manufacturer']
        mater.note=material['note']
        db.session.commit()
        return "success"
    else:
        return "failure"
def HnadleSubmitMaterialAddForm(material):
    mater = Material(name=material["name"], purity=material["purity"], manufacturer=material["manufacturer"],
                      note=material["note"])
    db.session.add(mater)
    db.session.commit()
    return "success"

def handleRemoveMaterial(mid):
    material = Material.query.filter_by(mid=mid).first()
    if material:
        db.session.delete(material)
        db.session.commit()
        return "success"
    else:
        return "failure"
def handleMaterialBatchDelete(midList):
    for mid in midList:
        material = Material.query.filter_by(mid=mid).first()
        if material:
            db.session.delete(material)
            db.session.commit()
    return "success"

def handleMaterialQueryContent(selectType,content,page,per_page):
    countQuery = "db.session.query(Material).filter(Material." + selectType + ".like('%" + content + "%')).count()"
    count = eval(countQuery)
    result = "db.session.query(Material).filter(Material." + selectType + ".like('%" + content + "%')).paginate(page=" + page + ", per_page=" + per_page + ", error_out=False)"
    materials = eval(result)
    materialInfo = {
        'materials': [a.to_json() for a in materials.items],
        'count': count
    }
    return json.dumps(materialInfo)