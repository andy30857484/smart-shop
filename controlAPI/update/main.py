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

def update(request):
    
    request_json = request.get_json()
    id = request_json['device']
    
    controlModel = ControlModel(**request_json)
    controlResponse.controlModel = request_json

    control = control_ref.document(id).get().to_dict()
    if(control != None):
            control_ref.document(id).set(controlModel.__dict__,merge=True)
            controlResponse.result ={
                    "code":"1",
                    "title":"修改完成",
                }
    else:
        controlResponse.controlModel = {}
        controlResponse.result ={
                "code":"-1",
                "title":"修改失敗",
                "description":"此電器("+str(id)+")尚未被建立"
            }
    
    return controlResponse.__dict__
