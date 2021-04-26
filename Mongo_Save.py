import pymongo
import json


class Peticiones_Mongo:
    def __init__(self, host):
        self.myclient = pymongo.MongoClient(f'mongodb://angeldavila:angeldavila@{host}/?authSource=admin')
        self.db = self.myclient['Base_de_Datos']
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
            json_sensor = {'id':sensor['id'],'nombre':sensor['nombre'],'clave':sensor['clave'],'tipoDato':sensor['tipoDato'],'pin':sensor['pin'],'lugar':sensor['lugar']}
            ArraySensores.append(json_sensor)
        return ArraySensores
