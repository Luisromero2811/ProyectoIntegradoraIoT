import requests


class chceckInternet:

    def check(self):
        try:
            request = requests.get('http://www.google.com', timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            print('sin conexion a internet...')
            return False
        else:
            print('conectado a internet')
            return True
