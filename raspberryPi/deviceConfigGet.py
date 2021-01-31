import firebase_admin
import model
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
lightModel = model.LightModel
a = input('please type device name:')
try:
    light_ref = db.collection(u'control').document(a)
except:
    print("can't find this device")
#gat lightModel from firebase
def lightGet():
    print("start lightGet")
    lstate=light_ref.get()
    lightDevice = lstate.to_dict()[u'device']
    lightPower = lstate.to_dict()[u'power']
    lightCost = lstate.to_dict()[u'cost']
    lightState = lstate.to_dict()[u'state']
    lightOnTime = lstate.to_dict()[u'onTime']
    lightOffTime = lstate.to_dict()[u'offTime']
    lightTotalCost = lstate.to_dict()[u'totalCost']
    lightTotalPower = lstate.to_dict()[u'totalPower']
    lightTurnOnTimes = lstate.to_dict()[u'threshold']
    lightAlertFlag = lstate.to_dict()[u'alertFlag']

    lightModel = {
        'device':lightDevice,
        'power':lightPower,
        'cost':lightCost,
        'state':lightState,
        'onTime':lightOnTime,
        'offTime':lightOffTime,
        'totalCost':lightTotalCost,
        'totalPower':lightTotalPower,
        'threshold':lightTurnOnTimes,
        'alertFlag':lightAlertFlag
        }

    print(lightModel)
    return lightModel

#send model to firebase
def lightSend(lightModel):
        light_ref.set(lightModel)
        
#after getting new parameters,update model
def updateModel(device,power,cost,state,onTime,offTime,totalCost,totalPower,threshold,alertFlag):
        model = {
        'device':device,
        'power':power,
        'cost':cost,
        'state':state,
        'onTime':onTime,
        'offTime':offTime,
        'totalCost':totalCost,
        'totalPower':totalPower,
        'threshold':threshold,
        'alertFlag':alertFlag
        }
        return model
    








