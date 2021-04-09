import pymongo
import json


class Peticiones_Mongo:
    def __init__(self, host):
        self.myclient = pymongo.MongoClient(f'mongodb://{host}/')
        self.db = self.myclient['Simsaweb']
        self.dbDatos = self.db['Datos']
        self.dbSensores = self.db['Sensores']

    def saveData(self, data):
        self.dbDatos.insert_many(data)

    def getSensores(self):
        ArraySensores = []
        sensores = self.dbSensores.find()
        for sensor in sensores:
            ArraySensores.append(sensor)
        return ArraySensores
