import json


class SaveJson:

    def __init__(self):
        self.data = {'Sensores': [], 'Datos': []}

    def store_json(self, data):
        self.data['Datos'].append(data)

        with open('data.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def save_sensors(self, sensores):
        self.data['Sensores'].append(sensores)

        with open('data.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def read_json(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read

    def getSensores(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read['Sensores']

    def getDatos(self):
        with open('data.json','r') as file:
            json_read = json.load(file)
        return json_read['Datos']

    def clean_Sensores(self):
        self.data['Sensores'] = []
        with open('data.json','w') as file:
            json.dump(self.data['Sensores'],file,indent=1)

    def clean_Datos(self):
        self.data['Datos']:[]