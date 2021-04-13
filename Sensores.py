from RPi import GPIO
import time
import datetime


class Sensores:

    def __init__(self):
        self.distancia = 0
        self.respuesta = []
        self.idsen = 0
        self.nombre = ''
        self.clave = ''
        self.pin = ''
        self.valor = 0
        self.fecha = 0
        self.tipoDato = None

    def ejecutar(self):
        if self.clave == 'hr-sr4':
            resp = self.ultrasonico()
            self.respuesta.append(resp)

    def setDatos(self, sensor):
        self.idsen = sensor['id']
        self.nombre = sensor['nombre']
        self.clave = sensor['clave']
        self.tipoDato = sensor['tipoDato']
        self.pin = sensor['pin']

    def cleerRespuesta(self):
        self.respuesta = []

    def ultrasonico(self):
        fecha_hora = str(datetime.datetime.now())[:19]
        GPIO.setmode(GPIO.BCM)

        puertos = self.pin.split(',')
        Trig = puertos[0]
        Echo = puertos[1]

        GPIO.setup(Trig, GPIO.OUT)
        GPIO.setup(Echo, GPIO.IN)
        GPIO.setwarnings(False)
        GPIO.output(Trig, True)
        time.sleep(0.00001)
        GPIO.output(Trig, False)

        while GPIO.input(Echo) == False:
            start = time.time()

        while GPIO.input(Echo) == True:
            end = time.time()

        sig_time = end - start

        # CM:
        distance = sig_time / 0.000058

        # inches:
        # distance = sig_time / 0.000148
        # print('Distance: {0:0.2f} centimeters'.format(distance))
        self.valor = distance
        self.fecha = fecha_hora
        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': distance, 'fecha': fecha_hora}

    def movimiento(self):
        # print(sensor['tipoDeDato'])
        GPIO.setmode(GPIO.BCM)
        GPIO_PIR = 18
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_PIR, GPIO.IN)
        fecha_hora = str(datetime.datetime.now())[:19]
        if GPIO.input(GPIO_PIR):
            # print("Se detecta  movimiento")
            valor = "Se detecto movimiento"
            time.sleep(1)
        else:
            # print("No hay movimiento")
            valor = "No hay movimiento..."
            time.sleep(1)

        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': valor, 'fecha': fecha_hora}

    def bomba(self):
        GPIO.setmode(GPIO.BCM)
        puertos = self.pin.split(',')
        GPIO_PIN = puertos[0]

        GPIO.setwarnings(False)
        GPIO.setup(GPIO_PIN,GPIO.OUT)

        if self.distancia <= 40:
            GPIO.input(GPIO_PIN)
        else:
            GPIO.output(GPIO_PIN)




GPIO.cleanup()
