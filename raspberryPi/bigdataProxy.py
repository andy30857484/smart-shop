import bigdataProxyConfig
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime


class BigdataProxy():

	def __init__(self):
		self.credentials = service_account.Credentials.from_service_account_file(bigdataProxyConfig.keyFile)
		self.projectId = bigdataProxyConfig.projectId
		self.client = bigquery.Client(project = self.projectId, credentials = self.credentials)
		self.datasetId = bigdataProxyConfig.datasetId

	def __insertRowToBigdata(self, tableId, insertData):
		table = self.client.dataset(self.datasetId).table(tableId)
		schema = self.client.get_table(table).schema
		result = self.client.insert_rows(table, insertData, selected_fields=schema)

	def injectAlertModel(self,lightModel):
		tableId = bigdataProxyConfig.tableId
		model = [{
            'device':lightModel['device'],
            'power':lightModel['power'],
            'cost':lightModel['cost'],
            'state':lightModel['state'],
            'onTime':lightModel['onTime'],
            'offTime':lightModel['offTime'],
            'totalCost':lightModel['totalCost'],
            'totalPower':lightModel['totalPower'],
            'threshold':lightModel['threshold'],
            'alertFlag':lightModel['alertFlag']
		}]

		self.__insertRowToBigdata(tableId,model)
		