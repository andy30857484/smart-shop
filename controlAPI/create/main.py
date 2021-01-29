import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from model import ControlModel, ControlResponse

controlModel = ControlModel()
controlResponse = ControlResponse()

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
control_ref = db.collection('control')

def create(request):
    request_json = request.get_json()
    id = request_json['device']

    controlModel = ControlModel(**request_json)
    controlResponse.controlModel = controlModel.__dict__

    control = control_ref.document(id).get().to_dict()

    if(control == None):
        control_ref.document(id).set(controlModel.__dict__)
        controlResponse.result = {
            "code": "1",
            "title": "電器建立完成",
        }
    else:
        controlResponse.result = {
            "code": "-1",
            "title": "重複註冊",
            "description": "此電器("+str(id)+")已被建立"
        }
    
    return controlResponse.__dict__

