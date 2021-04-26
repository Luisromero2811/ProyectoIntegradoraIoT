import json

import requests

url = 'http://3.143.15.255:3333/'


class Control:

    def checkPetLlenadoP(self, token):
        uri = url + 'LlenarP/Check'
        cabecera = {'authorization': 'Bearer ' + token}
        solicitud = requests.get(uri, headers=cabecera)

        if solicitud.status_code == 200:
            json_solicitud = json.loads(solicitud.text)
            return json_solicitud['data']
        else:
            print('Ocurrio un error')

    def EncenderRegado(self, token):
        uri = url + 'Regado/Encendido'
        cabecera = {'authorization': 'Bearer ' + token}
        solicitud = requests.get(uri, headers=cabecera)

        if solicitud.status_code == 200:
            json_solicitud = json.loads(solicitud.text)
            return json_solicitud['data']
        else:
            print('Ocurrio un error')
    
    def ApagarRegado(self, token):
        uri = url + 'Regado/Apagado'
        cabecera = {'authorization': 'Bearer ' + token}
        solicitud = requests.get(uri, headers=cabecera)

        if solicitud.status_code == 200:
            json_solicitud = json.loads(solicitud.text)
            return json_solicitud['data']
        else:
            print('Ocurrio un error')
    
    def CheckRegado(self, token):
        uri = url + 'Regado/Check'
        cabecera = {'authorization': 'Bearer ' + token}
        solicitud = requests.get(uri, headers=cabecera)

        if solicitud.status_code == 200:
            json_solicitud = json.loads(solicitud.text)
            print('request check:',json_solicitud)
            return json_solicitud['data']
        else:
            print('Ocurrio un error')