from app.models import Appliance
from app import db
import json

def handleGetAppliances(page,per_page):
    appliances = Appliance.query.paginate(page=page, per_page=per_page, error_out=False)
    res = db.engine.execute("select count(*) from appliance")
    count = [r[0] for r in res][0]
    applianceInfo={
        'appliances':[a.to_json() for a in appliances.items],
        'count':count
    }
    return json.dumps(applianceInfo)

def handleSummitApplianceEditForm(appliance):
    appli = Appliance.query.filter_by(aid=appliance['aid']).first()
    if appli:
        appli.name=appliance['name']
        appli.category=appliance['category']
        appli.manufacturer=appliance['manufacturer']
        appli.note=appliance['note']
        db.session.commit()
        return "success"
    else:
        return "failure"
def handleSummitApplianceAddForm(appliance):
    appli=Appliance(name=appliance["name"],category=appliance["category"],manufacturer=appliance["manufacturer"],note=appliance["note"])
    db.session.add(appli)
    db.session.commit()
    return "success"

def handleRemoveAppliance(aid):
    appliance = Appliance.query.filter_by(aid=aid).first()
    print(appliance)
    if appliance:
        db.session.delete(appliance)
        db.session.commit()
        return "success"
    else:
        return "failure"

def handleApplianceBatchDelete(aidList):
    for aid in aidList:
        appliance = Appliance.query.filter_by(aid=aid).pan
        if appliance:
            print(appliance.name)
            db.session.delete(appliance)
            db.session.commit()
    return "success"

def handleAppllianceQueryContent(selectType,content,page,per_page):
    query1="Appliance.query.filter_by(%s='%s').count()"%(selectType,content)
    print(query1)
    print("count:",eval(query1))
    query="Appliance.query.filter_by(%s='%s').paginate(page=%s, per_page=%s, error_out=False)"%(selectType,content,page,per_page)
    print(query)
    print(eval(query))
    return "success"