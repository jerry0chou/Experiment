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

def handleSubmitApplianceEditForm(appliance):
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

def handleSubmitApplianceAddForm(appliance):
    appli=Appliance(name=appliance["name"],category=appliance["category"],manufacturer=appliance["manufacturer"],note=appliance["note"])
    db.session.add(appli)
    db.session.commit()
    return "success"

def handleRemoveAppliance(aid):
    appliance = Appliance.query.filter_by(aid=aid).first()
    if appliance:
        db.session.delete(appliance)
        db.session.commit()
        return "success"
    else:
        return "failure"

def handleApplianceBatchDelete(aidList):
    for aid in aidList:
        appliance = Appliance.query.filter_by(aid=aid).first()
        if appliance:
            db.session.delete(appliance)
            db.session.commit()
    return "success"

def handleAppllianceQueryContent(selectType,content,page,per_page):
    countQuery="db.session.query(Appliance).filter(Appliance."+selectType+".like('%"+content+"%')).count()"
    count=eval(countQuery)
    result="db.session.query(Appliance).filter(Appliance."+selectType+".like('%"+content+"%')).paginate(page="+page+", per_page="+per_page+", error_out=False)"
    appliances=eval(result)
    applianceInfo = {
        'appliances': [a.to_json() for a in appliances.items],
        'count': count
    }
    return json.dumps(applianceInfo)

