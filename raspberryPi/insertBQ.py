from bigdataProxy import BigdataProxy

def insertBQ(newModel):
    BigdataProxy().injectAlertModel(newModel)
    print("instertBQ succeed")