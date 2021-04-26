import json

import requests

url = 'http://3.143.15.255:3333/'


class Control:

    def checkPetLlenadoP(self, token):
        try:
            uri = url + 'LlenarP/Check'
            cabecera = {'authorization': 'Bearer ' + token}
            solicitud = requests.get(uri, headers=cabecera)
            
            if solicitud.status_code == 200:
                json_solicitud = json.loads(solicitud.text)
                
                return json_solicitud['llenar']
            else:
                print('Ocurrio un error')
        except:
            print('No hay conexion con el servidor')

    def EncenderRegado(self, token):
        try:
            uri = url + 'Regado/Encendido'
            cabecera = {'authorization': 'Bearer ' + token}
            solicitud = requests.get(uri, headers=cabecera)

            if solicitud.status_code == 200:
                json_solicitud = json.loads(solicitud.text)
                return json_solicitud['data']
            else:
                print('Ocurrio un error')
        except:
            print('Ocurrio un error al iniciar el regado')
    
    def ApagarRegado(self, token):
        try:
            uri = url + 'Regado/Apagado'
            cabecera = {'authorization': 'Bearer ' + token}
            solicitud = requests.get(uri, headers=cabecera)

            if solicitud.status_code == 200:
                json_solicitud = json.loads(solicitud.text)
                return json_solicitud['data']
            else:
                print('Ocurrio un error')
        except:
            print('ocurrio un error al terminar el regado')
    
    def CheckRegado(self, token):
        try:
            uri = url + 'Regado/Check'
            cabecera = {'authorization': 'Bearer ' + token}
            solicitud = requests.get(uri, headers=cabecera)

            if solicitud.status_code == 200:
                json_solicitud = json.loads(solicitud.text)
                return json_solicitud['data']
            else:
                print('Ocurrio un error')
        except:
            print('ocurrio un error al verificar el estado')