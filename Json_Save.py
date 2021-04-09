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
