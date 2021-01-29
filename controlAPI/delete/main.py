import os
from firebase_admin import credentials, firestore, initialize_app
import requests
import json
from model import ControlModel,ControlResponse

controlModel = ControlModel()
controlResponse = ControlResponse()

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
control_ref = db.collection('control')

def delete(request):
    
    request_json = request.get_json()
    id = request_json['device']
    
    controlResponse.controlModel = {}
    
    control = control_ref.document(id).get().to_dict()
    
    if(control != None):
        control_ref.document(id).delete()
        controlResponse.result ={
                "code":"1",
                "title":"已刪除此電器",
            }
    else:
        controlResponse.result ={
                "code":"-1",
                "title":"無相關資料",
            }
    return controlResponse.__dict__
