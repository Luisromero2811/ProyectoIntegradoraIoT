import requests

import speedtest


class chceckInternet:

    def check(self):
        try:
            request = requests.get('http://www.google.com', timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            print('sin conexion a internet...')
            return False
        else:
            print('conectado a internet')
            """s = speedtest.Speedtest()
            down = round((round(s.download())/ 1048576), 2)
            upload = round((s.upload()/ 1048576), 2)
            print(f'download:{down}  upload:{upload}')"""
            return True
