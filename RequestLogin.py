import json

import requests

url = 'http://3.143.15.255:3333/'
email = 'raspberry@gmail.com'
passw = 12345678


class Request:
    
    def request(self):
        uri = url + 'Registro'

        datos = {'email': email, 'password': passw}
        solicitudR = requests.post(uri, params=datos)

        if solicitudR.status_code == 201:
            uri = url + 'Login'
            solicitudL = requests.post(uri, params=datos)

            if solicitudL.status_code == 200:
                response_json = json.loads(solicitudL.text)
                return response_json['token']
            else:
                print('credenciales incorrectas...')
                return False

        else:
            print('Formato incorrecto...')
            return False
