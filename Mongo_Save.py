import pymongo
import json


class Peticiones_Mongo:
    def __init__(self, host):
        self.myclient = pymongo.MongoClient(f'mongodb://{host}/')
        self.db = self.myclient['Simsaweb']
        self.dbDatos = self.db['Datos']
        self.dbSensores = self.db['Sensores']

    def saveSensores(self, data):
        self.dbSensores.insert_many(data)

    def saveDatos(self,data):
        self.dbDatos.insert_many(data)

    def getSensores(self):
        ArraySensores = []
        sensores = self.dbDatos.find()
        for sensor in sensores:
            json_sensor = {'id':sensor['id'],'nombre':sensor['nombre'],'clave':sensor['clave'],'tipoDato':sensor['tipoDato'],'pin':sensor['pin']}
            ArraySensores.append(json_sensor)
        return ArraySensores
