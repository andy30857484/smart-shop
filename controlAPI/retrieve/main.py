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


def retrieve(request):
    
    request_args = request.args
    if(request.args and 'device' in request.args):
        id = request.args.get('device')
        control = control_ref.document(id).get().to_dict()
        if(control != None):
            controlResponse.controlModel = control
            controlResponse.result ={
                    "code":"1",
                    "title":"已為您查詢電器",
                }
        else:
            controlResponse.controlModel = {}
            controlResponse.result ={
                    "code":"-1",
                    "title":"無相關資料",
                    "description":"此電器("+str(id)+")尚未被建立"
                }
    else:
        controlResponse.controlModel = [doc.to_dict() for doc in control_ref.stream()]
        controlResponse.result ={
                    "code":"1",
                    "title":"所有電器列表",
                }
    return controlResponse.__dict__
