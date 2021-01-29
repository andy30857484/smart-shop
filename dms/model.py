class ControlModel():
    def __init__(self, device=None,power=None,cost=None,state=None
    ,onTime=None,offTime=None,totalCost=None,totalPower=None,threshold=None,
    alertFlag=None):
        self.device = device
        self.power = power
        self.cost = cost
        self.state = state
        self.onTime = onTime
        self.offTime = offTime
        self.totalCost = totalCost
        self.totalPower = totalPower
        self.threshold = threshold
        self.alertFlag = alertFlag


class ControlResponse():
    def __init__(self, controlModel=None, result=None):
        self.controlModel = controlModel
        self.result = result
