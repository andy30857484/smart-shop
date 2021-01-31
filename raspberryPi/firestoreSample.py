import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebaseKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

status_ref = db.collection(u'control').document(u'gg')

try:
        status=status_ref.get()
        print(format(status.to_dict()[u'state']))
except:
        print("no data found!!!")



GPIO.setmode(GPIO.BCM)
#GPIO.setup(26,GPIO.OUT)

