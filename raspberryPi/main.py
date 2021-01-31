import time
import deviceConfigGet
import deviceControl
import insertBQ
import linePush

while True:
    #get model from firestore
    lightModel = deviceConfigGet.lightGet()
    #get parameters
    device = lightModel['device']
    power = lightModel['power']
    cost = lightModel['cost']
    state = lightModel['state']
    onTime = lightModel['onTime']
    offTime = lightModel['offTime']
    totalCost = lightModel['totalCost']
    totalPower = lightModel['totalPower']
    threshold = lightModel['threshold']
    alertFlag = lightModel['alertFlag']
    
#control LED light
    deviceControl.light(state,device)
#get onTime,offTime
    onTime,offTime = deviceControl.lightGetTime(onTime,offTime,state)
#get power,cost
    power,cost,canIteration = deviceControl.lightCount(onTime,offTime,power,cost,state)
#get totalPower,totalCost
    totalPower,totalCost = deviceControl.deviceIteration(totalPower,totalCost,power,cost,canIteration)
#get alertFlag
    alertFlag = deviceControl.tatalPowerAlert(threshold,totalCost,alertFlag)
#turn onTime,offTime into timeStamp
    onTime,offTime = deviceControl.dateTransForm(onTime,offTime)
#linePushAlert
    linePush.linePush(totalCost,alertFlag)
#updateModel    
    newModel = deviceConfigGet.updateModel(device,power,cost,state,onTime,offTime,totalCost,totalPower,threshold,alertFlag)
    print(newModel)
#send newModel to firebase
    deviceConfigGet.lightSend(newModel)
#send newModel to BigQuery    
    insertBQ.insertBQ(newModel)
    time.sleep(2)
