from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
devices_ref = db.collection('devices')

def createDevice(request):
    devices_ref.document(request['device']).set(request)

def updateDevice(request):
    devices_ref.document(request['device']).update({'staff':request['staff']})
    devices_ref.document(request['device']).update({'manager':request['manager']})
    devices_ref.document(request['device']).update({'customer':request['customer']})


def queryDevice():
    return list(doc.to_dict() for doc in devices_ref.stream())

def queryStaffDevice(request):
    return list(doc.to_dict() for doc in devices_ref.where('staff.uid', '==', request['uid']).stream())

def playbackSecondUpdate(request):
    devices_ref.document(request['device']).update({'config.capture.streaming.playbackSecond':request['config']['capture']['streaming']['playbackSecond']})

def captureTypeUpdate(request):
    devices_ref.document(request['device']).update({'config.capture.streaming.type':request['config']['capture']['streaming']['type']})

def captureSourceUpdate(request):
    devices_ref.document(request['device']).update({'config.capture.streaming.' + request['config']['capture']['streaming']['typeName'][0] + '.' + request['config']['capture']['streaming']['typeName'][1]  :request['config']['capture']['streaming']['source']})


def recognitionUpdate(request):
    devices_ref.document(request['device']).update({'config.recognition.' + request['alertType'] :request['config']['recognition']})

def alertUpdate(request):
    devices_ref.document(request['device']).update({'config.alert':request['config']['alert']})

def operationModeUpdate(request):
    devices_ref.document(request['device']).update({'operation.mode':request['operation']['mode']})

def operationActivationUpdate(request):
    devices_ref.document(request['device']).update({'operation.activation':request['operation']['activation']})

def notificationActivationUpdate(request):
    devices_ref.document(request['device']).update({'config.notification.activation':request['config']['notification']['activation']})

def notificationUpdate(request):
    devices_ref.document(request['device']).update({'config.notification.interval':request['config']['notification']['interval']})

# def queryDeviceData(device):
#     return devices_ref.document(device).get().to_dict()