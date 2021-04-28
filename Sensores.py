import time
import json
import datetime
from RPi import GPIO
from smbus2 import SMBus, i2c_msg

class Sensores:

    def __init__(self):
        self.data = {'doneLlenado':False,'doneRegado':False,'doneMove':False}
        self.dataSensores = {'NivelP':0,'NivelS':0,'Humedad':0}

        self.distancia = 0

        self.distanciaP = 0
        self.distanciaS = 0

        self.banderaP = False
        self.banderaR = False
        self.banderaM = False

        self.humedad = 0
        
        self.peticionLlenadoP = 0
        self.peticionLlenadoS = 0

        self.respuesta = []
        self.done = []

        self.idsen = 0
        self.nombre = ''
        self.clave = ''
        self.pin = ''
        self.valor = 0
        self.fecha = 0
        self.tipoDato = None
        self.lugar = ''

    def ejecutar(self):
        if self.clave == 'hr-sr4':
            resp = self.ultrasonico()
            self.respuesta.append(resp)
            return self.valor
        elif self.clave == 'bomba':
            resp = self.bomba()
            self.respuesta.append(resp)
        elif self.clave == 'hl-69':
            resp = self.humedad_tierra()
            self.respuesta.append(resp)
        elif self.clave == 'pir':
            resp = self.movimiento()
            self.respuesta.append(resp)

    def setDatos(self, sensor, bandera, Pila):
        self.idsen = sensor['id']
        self.nombre = sensor['nombre']
        self.clave = sensor['clave']
        self.tipoDato = sensor['tipoDato']
        self.pin = sensor['pin']
        self.lugar = sensor['lugar']
        self.banderaR = bandera
        self.banderaP = Pila

    def cleerRespuesta(self):
        self.respuesta = []
    
    def getRespuestas(self):
        return self.respuesta

    def ultrasonico(self):
        fecha_hora = str(datetime.datetime.now())[:19]
        try:
            
            GPIO.setmode(GPIO.BCM)

            puertos = self.pin.split(',')
            
            Trig = int(puertos[0])
            Echo = int(puertos[1])

            GPIO.setup(Echo,GPIO.IN)
            GPIO.setup(Trig,GPIO.OUT)

                
            GPIO.output(Trig,False)
            time.sleep(0.5)
                        
            GPIO.output(Trig,True)
            time.sleep(0.00001)
            GPIO.output(Trig,False)

            while GPIO.input(Echo) == 0:
                START = time.time()

            while GPIO.input(Echo) == 1:
                END = time.time()

            duracion = START - END

            distancia = duracion * 17150
            self.distancia = (round(distancia, 2)*-1)
        except:
            print('ocurrio un error al obtener la distancia')
        """# CM:
        self.distancia = sig_time / 0.000058"""
        
        #self.valor = int(100 - ((self.distancia*100)/100))
        self.fecha = fecha_hora
        print('distanciaz:',self.distancia)
        if self.lugar == 'NivelP':
            self.valor = int(100 - ((self.distancia*100)/25))
            self.distanciaP = self.valor
            self.dataSensores['NivelP'] = self.valor

        elif self.lugar == 'NivelS':
            self.valor = int(100 - ((self.distancia*100)/25))
            self.distanciaS = self.valor
            self.dataSensores['NivelS'] = self.valor
        
        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}

    def checkDone(self,maxDistance,maxHumedad):
        
        if self.banderaP and int(maxDistance) <= self.valor:
            self.data['doneLlenado'] = True
        if self.humedad >= int(maxHumedad) and self.banderaR:
            self.data['doneRegado'] = True
        if self.valor == 'Se detecto movimiento' and self.banderaM:
            self.data['doneMove'] = True
        return self.data

    def resetDoneL(self):
        self.data['doneLlenado'] = False

    def resetDoneR(self):
        self.data['doneRegado'] = False
    
    def resetDoneM(self):
        self.data['doneMove'] = False

    def movimiento(self):
        # print(sensor['tipoDeDato'])
        try:
            GPIO.setmode(GPIO.BCM)
            puertos = self.pin.split(',')
            pin = int(puertos[0])
            GPIO_PIR = pin
            GPIO.setwarnings(False)
            GPIO.setup(GPIO_PIR, GPIO.IN)
            fecha_hora = str(datetime.datetime.now())[:19]
            
            #GPIO.add_event_detect(GPIO_PIR,GPIO.RISING,self.detectMove)
            if GPIO.input(GPIO_PIR):
                # print("Se detecta  movimiento")
                self.valor = "Se detecto movimiento"
                self.banderaM = True
                #time.sleep(1)
        except:
            print('Ocurrio un error en el sensor')

        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}
    

    def bomba(self):
        try:
            pin = self.pin.split(',')
            addr = int(pin[0])
            pinout = int(pin[1])
            fecha_hora = str(datetime.datetime.now())[:19]
            with SMBus(1) as bus:
                if self.lugar == 'NivelP':
                    data = self.comparacion_bomba(self.banderaP,'NivelP',pinout)
                
                if self.lugar == 'NivelS':
                    data = self.comparacion_bomba(self.banderaR,'NivelS',pinout)
                
                data = data.encode()
                bus.write_i2c_block_data(addr,0,data)
                
        except:
            print('ocurrio un error al encender la bomba')
        
        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}

    def comparacion_bomba(self,flag,lugar,pinout):
        if self.lugar == lugar:
            if flag:
                data = f'{self.lugar},{pinout},on' + '\n'
                return data
            else:
                data = f'{self.lugar},{pinout},off' + '\n'
                return data

    def humedad_tierra(self,*args):
        try:
            pin = self.pin.split(',')
            addr = int(pin[0])
            data = ''
            fecha_hora = str(datetime.datetime.now())[:19]
            with SMBus(1) as bus:
            
                """LED = input('>>>>>  ')
                LED = LED + '\n'
                LED = LED.encode()
                bus.write_i2c_block_data(31,0,LED)"""
                
                data = bus.read_i2c_block_data(31,0x00,16)
                self.valor = data[0]
                self.humedad = self.valor
                self.dataSensores['Humedad'] = self.valor
            
            return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}
                
        except:
            print('sin conexion con arduino')
        
    def getDataSensores(self):
        return self.dataSensores
    
    def setAltura(self):
        altura = 0
        for _ in range(1,3):
            altura += (self.ultrasonico())['valor']
        altura = altura / 3
        print('altura: ', altura)

    def getDone(self):
        done = []




#GPIO.cleanup()
