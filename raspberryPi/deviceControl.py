import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)

#control LED light
def light(state,device):
    if state == '1' and device == 'light':
        time.sleep(0.5)
        GPIO.output(3,1)
        print("light has been opened")
    if state == '1' and device == 'ac':
        time.sleep(0.5)
        GPIO.output(4,1)
        print("ac has been opened")
    if state == '0' and device == 'light':
        time.sleep(0.5)
        GPIO.output(3,0)
        print("light has been closed")
    if state == '0' and device == 'ac':
        time.sleep(0.5)
        GPIO.output(4,0)
        print("ac has been closed")
       
#update onTime,offTime
def lightGetTime(onTime,offTime,state):
    onTime = time.mktime(time.strptime(onTime,'%Y-%m-%d %H:%M:%S'))
    offTime = time.mktime(time.strptime(offTime,'%Y-%m-%d %H:%M:%S'))
    if state == '1':
        onTime = int(time.time())
    if state == '0':
        offTime = int(time.time())
    return onTime,offTime
    
#update power,cost
def lightCount(onTime,offTime,power,cost,state):
    if onTime == 87:
        print("it hasn't been turned on")
    if offTime == 87:
        print("it hasn't been turned off")
    if onTime != 87 and offTime != 87 and offTime < onTime and state == '1':
        sec = onTime - offTime
        hr = sec/60
        power = 60/1000*hr #kw*hr
        cost = power*5
        canIteration = True
        print('count power,cost success')
        return power,cost,canIteration
    else:
        canIteration = False
        return power,cost,canIteration
        
#update totalPower,totalCost
def deviceIteration(totalPower,totalCost,power,cost,canIteration):
    try:
        if canIteration == True:
            totalPower = int(totalPower + power)
            totalCost = int(totalCost + cost)
        print("Iteration Sucessecd")
    except:
        print("Iteration faild")
    return totalPower,totalCost

#update alertFlag
def tatalPowerAlert(threshold,totalCost,alertFlag):
    try:
        totalCost = int(totalCost)
        threshold = int(threshold)
        if totalCost > threshold:
            alertFlag = 'True'
        else:
            alertFlag = 'False'
    except:
        print("totalPower or threshold is not intable!")
    
    return alertFlag

def dateTransForm(onTime,offTime):
    dOnTime = datetime.datetime.fromtimestamp(onTime).strftime('%Y-%m-%d %H:%M:%S')
    dOffTime = datetime.datetime.fromtimestamp(offTime).strftime('%Y-%m-%d %H:%M:%S')
    return dOnTime,dOffTime
    





