import pymongo
import json


class Peticiones_Mongo:
    def __init__(self, host):
        try:
            self.myclient = pymongo.MongoClient(f'mongodb://angeldavila:angeldavila@{host}/?authSource=admin')
            self.db = self.myclient['Base_de_Datos']
            self.dbDatos = self.db['Datos']
            self.dbSensores = self.db['Sensores']
        except:
            print('ocurrio un error al conectar con mongo')

    def saveSensores(self, data):
        try:
            self.dbSensores.insert_many(data)
        except:
            print('ocurrio un error al guardar los sensores')

    def saveDatos(self,data):
        try:
            self.dbDatos.insert_many(data)
        except:
            print('ocurrio un error al guardar los datos')

    def getSensores(self):
        ArraySensores = []
        try:
            sensores = self.dbDatos.find()
            for sensor in sensores:
                json_sensor = {'id':sensor['id'],'nombre':sensor['nombre'],'clave':sensor['clave'],'tipoDato':sensor['tipoDato'],'pin':sensor['pin'],'lugar':sensor['lugar']}
                ArraySensores.append(json_sensor)
            return ArraySensores
        except:
            print('ocurrio un error al obtener los sensores')
            return ArraySensores