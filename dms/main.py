from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import Flask, render_template, session, request, redirect, url_for
import requests
import importlib
import json
import os
from datetime import datetime
import firestoreApi
import time
from model import ControlModel
import controlConfig


app = Flask(__name__)
controlModel=ControlModel


#------------------controlCreate----------------
@app.route("/dms/control/create",methods = ['GET','POST'])
def controlcreate():
    global controlModel

    if request.method == 'GET':
        return render_template('controlCreateRequest.html',controlModel=controlModel)
    if request.method == 'POST':
        ControlModel={
            "device":request.values['device'],
            "power":0,
            "cost":0,
            "state":request.values['state'],
            "onTime":87,
            "offTime":87,
            "totalCost":0,
            "totalPower":0,
            "threshold":0,
            "alertFlag":False}

        controlModel = ControlModel

        apiResponse = requests.post(controlConfig.createApi, json=controlModel)
        print("!!!")
        print(apiResponse)
        print("!!!")
        controlResponse = apiResponse.json()
        return render_template('controlCreateRequest.html', controlModel = controlResponse, method = request.method) 


#------------------controlDelete----------------
@app.route("/dms/control/delete",methods = ['GET','POST'])
def controlDelete():
    global controlModel

    if request.method == 'GET':
        return render_template('controlDeleteRequest.html',controlModel=controlModel)
    if request.method == 'POST':
        controlModel = ControlModel(device=request.values['device'])

        controlResponse = requests.delete(
            controlConfig.deleteApi, json=controlModel.__dict__)

        controlResponse = controlResponse.json()

        if controlResponse['result']['code'] == "1":
            return render_template("controlDeleteResponse.html", controlModel=controlResponse)
        else:
            return render_template("controlDeleteFail.html", result=controlResponse)


#------------------controlList----------------
@app.route('/dms/control/list', methods=['GET', 'POST'])
def controlList():
    apiResponse = requests.get(controlConfig.listApi)

    controlResponse = apiResponse.json()
    controlLength = len(controlResponse['controlModel'])

    return render_template('controlListResponse.html', controlModel=controlResponse, length=controlLength)

#------------------controlQuery----------------
@app.route('/dms/control/query', methods=['GET', 'POST'])
def controlQuery():
    if request.method == "GET":
        return render_template("controlQueryRequest.html")
    if request.method == "POST":
        apiResponse = requests.get(controlConfig.queryApi+'?device='+request.values['device'])

        controlResponse = apiResponse.json()
        if controlResponse['controlModel']!={}:
            return render_template('controlQueryResponse.html', controlModel=controlResponse)
        else:
            return render_template('controlQueryFail.html', controlModel=controlResponse)


#------------------controlUpdate----------------
@app.route('/dms/control/update', methods=['GET', 'POST'])
def controlUpdate():
    global controlModel
    if request.method == "GET":
        print(controlModel)
        return render_template("controlQueryRequest.html")
    if request.method == "POST":
        try:
            ControlModel = {
                'device' : request.values['device'],
                'power' : request.values['power'],
                'cost' : request.values['cost'],
                'state' : request.values['state'],
                'onTime' : request.values['onTime'],
                'offTime' : request.values['offTime'],
                'totalCost' : request.values['totalCost'],
                'totalPower' : request.values['totalPower'],
                'threshold' : int(request.values['threshold']),
                'alertFlag' : request.values['alertFlag']
            }
            Cpower = float(ControlModel['power'])
            Ccost = float(ControlModel['cost'])
            #ConTime = int(ControlModel['onTime'])
            #CoffTime = int(ControlModel['offTime'])
            CtotalCost = float(ControlModel['totalCost'])
            CtotalPower = float(ControlModel['totalPower'])
            Cthreshold = int(ControlModel['threshold'])
            Cmodel = {
                'device' : ControlModel['device'],
                'power' : Cpower,
                'cost' : Ccost,
                'state' : ControlModel['state'],
                'onTime' : ControlModel['onTime'],
                'offTime' : ControlModel['offTime'],
                'totalCost' : CtotalCost,
                'totalPower' : CtotalPower,
                'threshold' : Cthreshold,
                'alertFlag' : ControlModel['alertFlag']
            }
            controlModel = Cmodel
            apiResponse = requests.put(controlConfig.updateApi, json=controlModel)
            print(apiResponse)
            controlResponse = apiResponse.json()
            print(controlResponse)

            if controlResponse['controlModel']!={}:
                return render_template('controlUpdateResponse.html', controlModel=controlResponse)
        except:
            apiResponse = requests.get(controlConfig.queryApi+'?device='+request.values['device'])
            controlResponse = apiResponse.json()
            if controlResponse['controlModel']!={}:
                return render_template('controlUpdateRequest.html', controlModel=controlResponse)
            else:
                return render_template('controlQueryFail.html', controlModel=controlResponse)


#------------------deviceCreate----------------
@app.route("/dms/device/create",methods = ['GET','POST'])
def deviceCreate():
    if request.method == 'GET':
        return render_template('createDeviceRequest.html')
    if request.method == 'POST':    
        configModel={
            "capture":{
                "streaming":{
                    "type":0,
                    "playbackSecond":10,
                    "rtsp":{
                        "ip":""
                    },
                    "dash":{
                        "url":""
                    },
                    "camera":{
                        "index":""
                    }
                }
            },
            "recognition":{
                "Whole":{
                    "onDuty":{
                        "alertBeginTime":'09:00',
                        "alertEndTime":'18:00',
                        "threshold":1
                    },
                    "offDuty":{
                        "alertBeginTime":'18:01',
                        "alertEndTime":'23:00',
                        "threshold":1
                    },
                    "curfew":{
                        "alertBeginTime":'23:01',
                        "alertEndTime":'08:59',
                        "threshold":1
                    }
                },
                "Region":{
                    "onDuty":{
                        "alertBeginTime":'09:00',
                        "alertEndTime":'18:00',
                        "threshold":1
                    },
                    "offDuty":{
                        "alertBeginTime":'18:01',
                        "alertEndTime":'23:00',
                        "threshold":1
                    },
                    "curfew":{
                        "alertBeginTime":'23:01',
                        "alertEndTime":'08:59',
                        "threshold":1
                    }
                },
                "Line":{
                    "onDuty":{
                        "alertBeginTime":'09:00',
                        "alertEndTime":'18:00',
                        "threshold":1
                    },
                    "offDuty":{
                        "alertBeginTime":'18:01',
                        "alertEndTime":'23:00',
                        "threshold":1
                    },
                    "curfew":{
                        "alertBeginTime":'23:01',
                        "alertEndTime":'08:59',
                        "threshold":1
                    }
                },
                "Point":{
                    "onDuty":{
                        "alertBeginTime":'09:00',
                        "alertEndTime":'18:00',
                        "threshold":2
                    },
                    "offDuty":{
                        "alertBeginTime":'18:01',
                        "alertEndTime":'23:00',
                        "threshold":1
                    },
                    "curfew":{
                        "alertBeginTime":'23:01',
                        "alertEndTime":'08:59',
                        "threshold":0
                    }
                }
            },
            "alert":{
                "regionCoordinate":{           
                    "upperLeftPointX":250,
                    "upperLeftPointY":120,
                    "lowerRightPointX":380,
                    "lowerRightPointY":185
                },
                "point1Coordinate":{
                    "pointX":350,
                    "pointY":350
                },
                "point2Coordinate":{
                    "pointX":420,
                    "pointY":300
                },
                "lineCoordinate":{
                    "upperPointX":320,
                    "upperPointY":0,
                    "lowerPointX":320,
                    "lowerPointY":480
                }
            },
            "notification":{
                "interval":10,
                "activation":True
            }
        }

        staffModel={
            "name":request.values["staff"],
            "lineId":request.values["lineId"]
        }

        acModel={
            "acName":request.values['acName'],
            "operation":{
                "activation":False
            },

            "powerUsed":{
                "kwhr": '88',
                "cost": '88'
            }
        }


        

        firestoreApi.createDevice(deviceModel)

        return render_template('createDeviceRequest.html',method = request.method )


#------------------streamingUpdate----------------
@app.route("/dms/streaming/update",methods = ['GET','POST'])
def streamingUpdate():
    if request.method == 'GET':
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceStreamingRequest.html', deviceModel=deviceResponse)

    if request.method == 'POST':
        if request.values['captureSourceType'] =='0':
            typeName = ['rtsp','ip']
        elif request.values['captureSourceType']=='1':
            typeName = ['dash','url']
        else:
            typeName = ['camera','index']

        captureModel={
            "streaming":{
                "playbackSecond":int(request.values['playbackSecond']),
                "type":int(request.values['captureSourceType']),
                "typeName":typeName,
                "source":request.values['source']
            }   
        }
        
        deviceModel = {
            "device":request.values['device'],
            "config":{
                "capture":captureModel
            }
        }

        firestoreApi.playbackSecondUpdate(deviceModel)
        firestoreApi.captureTypeUpdate(deviceModel)
        firestoreApi.captureSourceUpdate(deviceModel)

        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceStreamingRequest.html',deviceModel = deviceResponse,  method = request.method)


#------------------recognitionUpdate----------------
@app.route("/dms/recognition/update",methods = ['GET','POST'])
def recognitionUpdate():
    if request.method == 'GET':
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceRecognitionRequest.html', deviceModel=deviceResponse)
    if request.method == 'POST':

        recognitionModel = {     
            "onDuty":{
                "alertBeginTime":request.values['onDutyAlertBeginTime'],
                "alertEndTime":request.values['onDutyAlertEndTime'],
                "threshold":int(request.values['onDutyThreshold'])
            },
            "offDuty":{
                "alertBeginTime":request.values['offDutyAlertBeginTime'],
                "alertEndTime":request.values['offDutyAlertEndTime'],
                "threshold":int(request.values['offDutyThreshold'])
            },
            "curfew":{
                "alertBeginTime":request.values['curfewAlertBeginTime'],
                "alertEndTime":request.values['curfewAlertEndTime'],
                "threshold":int(request.values['curfewThreshold'])
            }
        }

        deviceModel = {
            "device":request.values['device'],
            "alertType":request.values['selectedAlertType'],
            "config":{
                "recognition":recognitionModel
            }
        }

        firestoreApi.recognitionUpdate(deviceModel)

        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceRecognitionRequest.html', deviceModel = deviceResponse , method = request.method)  


#------------------alertUpdate----------------
@app.route("/dms/alert/update",methods = ['GET','POST'])
def alertUpdate():
    if request.method == 'GET':
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceAlertRequest.html', deviceModel=deviceResponse)
    if request.method == 'POST':
        alertModel={
            "regionCoordinate":{
                "upperLeftPointX": int(request.values['upperLeftPointX']),
                "upperLeftPointY": int(request.values['upperLeftPointY']),
                "lowerRightPointX": int(request.values['lowerRightPointX']),
                "lowerRightPointY": int(request.values['lowerRightPointY'])
            },
            "point1Coordinate":{
                "pointX":int(request.values['pointX1']),
                "pointY":int(request.values['pointY1'])
            },
            "point2Coordinate":{
                "pointX":int(request.values['pointX2']),
                "pointY":int(request.values['pointY2'])
            },
            "lineCoordinate":{
                "upperPointX": int(request.values['upperPointX']),
                "upperPointY": int(request.values['upperPointY']),
                "lowerPointX": int(request.values['lowerPointX']),
                "lowerPointY": int(request.values['lowerPointY'])
            }
        }

        deviceModel = {
            "device":request.values['device'],
            "config":{
                "alert": alertModel
            }
        }

        firestoreApi.alertUpdate(deviceModel)
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceAlertRequest.html', deviceModel = deviceResponse, method = request.method) 


#------------------operationActivationUpdate----------------
@app.route("/dms/operationActivation/update",methods = ['GET','POST'])
def operationActivate():
    if request.method == 'GET':
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceOperationRequest.html', deviceModel=deviceResponse)
    if request.method == 'POST':
        operationModel={
            "activation":True if request.values['activation']=='1' else False,
        }
        deviceModel = {
            "device":request.values['device'],
            "operation": operationModel
        }

        firestoreApi.operationActivationUpdate(deviceModel)
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceOperationRequest.html', deviceModel =deviceResponse, method = request.method )


#------------------notificationUpdate---------------
@app.route("/dms/notification/update",methods = ['GET','POST'])
def notificationUpdate():
    if request.method == 'GET':
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceNotificationRequest.html', deviceModel=deviceResponse)
    if request.method == 'POST':
        notificationModel={
            "interval":int(request.values['interval']),
        }
        
        deviceModel = {
            "device":request.values['device'],
            "config":{
                "notification":notificationModel
            }
        }

        firestoreApi.notificationUpdate(deviceModel)
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceNotificationRequest.html',deviceModel = deviceResponse, method = request.method)


#------------------notificationActivationUpdate---------------
@app.route("/dms/notificationActivation/update",methods = ['GET','POST'])
def notificationActivate():
    if request.method == 'POST':
        notificationModel={
            "activation":True if request.values['activation']=='1' else False,
        }
        deviceModel = {
            "device":request.values['device'],
            "config": {
                "notification" : notificationModel
            }
        }

        firestoreApi.notificationActivationUpdate(deviceModel)
        deviceResponse = firestoreApi.queryDevice()
        return render_template('updateDeviceNotificationRequest.html', deviceModel =deviceResponse, method = request.method )







if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)