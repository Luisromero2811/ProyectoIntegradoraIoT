import json


class SaveJson:

    def __init__(self):
        self.data = {'Sensores': [], 'Datos': []}

    def store_json(self, data):
        for sensor in data:
            self.data['Datos'].append(sensor)

        with open('data.json', 'w') as file:
            json.dump(self.data['Datos'], file, indent=4)

    def save_sensors(self, sensores):
        for data in sensores:
            self.data['Sensores'].append(data)

        with open('dataSen.json', 'w') as file:
            json.dump(self.data['Sensores'], file, indent=4)
    
    def saveAll(self):
        with open('data.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def read_json(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read

    def getSensores(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read#['Sensores']

    def getDatos(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read#['Datos']

    def clean_Sensores(self):
        self.data['Sensores']:[]
        print('limpiando sensores')
        with open('dataSen.json','w') as file:
            json.dump(self.data['Sensores'],file)

    def clean_Datos(self):
        self.data['Datos']:[]
        print('limpiando datos')
        with open('data.json','w') as file:
            json.dump(self.data['Datos'],file)