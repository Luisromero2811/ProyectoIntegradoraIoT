import time
import datetime
from RPi import GPIO
from smbus2 import SMBus, i2c_msg

class Sensores:

    def __init__(self):
        self.dataSensores = {'NivelP':0,'NivelS':0,'Humedad':0}

        self.distancia = 0

        self.distanciaP = 0
        self.distanciaS = 0

        self.banderaP = False
        self.banderaS = False

        self.humedad = 0
        
        self.peticionLlenadoP = 10
        self.peticionLlenadoS = 0

        self.respuesta = []

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
            print('respuesta sensor de tierra',resp)
            self.respuesta.append(resp)

    def setDatos(self, sensor, bandera):
        self.idsen = sensor['id']
        self.nombre = sensor['nombre']
        self.clave = sensor['clave']
        self.tipoDato = sensor['tipoDato']
        self.pin = sensor['pin']
        self.lugar = sensor['lugar']
        self.banderaP = bandera

    def cleerRespuesta(self):
        self.respuesta = []
    
    def getRespuestas(self):
        return self.respuesta

    def ultrasonico(self):
        
        fecha_hora = str(datetime.datetime.now())[:19]
        GPIO.setmode(GPIO.BCM)

        puertos = self.pin.split(',')
        Trig = int(puertos[0])
        Echo = int(puertos[1])

        GPIO.setup(Trig,GPIO.OUT)
        GPIO.setup(Echo,GPIO.IN)

        
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
                
        """# CM:
        self.distancia = sig_time / 0.000058
        print(self.distancia)"""
        self.valor = int(100 - ((self.distancia*100)/100))
        self.fecha = fecha_hora

        if self.lugar == 'NivelP':
            self.distanciaP = self.valor
            self.dataSensores['NivelP'] = self.valor

        elif self.lugar == 'NivelS':
            self.distanciaS = self.valor
            self.dataSensores['NivelS'] = self.valor
            

        # inches:
        # distance = sig_time / 0.000148
        #print('Distance: {0:0.2f} centimeters'.format(self.distancia))
        #print(int((self.distancia*100)/3000))

        
        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}

    def movimiento(self):
        # print(sensor['tipoDeDato'])
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO_PIR = 18
            GPIO.setwarnings(False)
            GPIO.setup(GPIO_PIR, GPIO.IN)
            fecha_hora = str(datetime.datetime.now())[:19]
            if GPIO.input(GPIO_PIR):
                # print("Se detecta  movimiento")
                self.valor = "Se detecto movimiento"
                #time.sleep(1)
        except:
            print('Ocurrio un error en el sensor')

        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}
    
    
    def bomba(self):
        try:
            GPIO.setmode(GPIO.BCM)
            puertos = self.pin.split(',')
            GPIO_PIN = int(puertos[0])
            print(GPIO_PIN)
            fecha_hora = str(datetime.datetime.now())[:19]

            GPIO.setwarnings(False)
            GPIO.setup(GPIO_PIN,GPIO.OUT)

            if self.distanciaP > 0 and self.lugar == 'NivelP' and self.banderaP == True and self.humedad < 100:
                print(f'distancia {self.distancia}')
                print('bomba encendida')
                GPIO.output(GPIO_PIN,GPIO.HIGH)
                self.valor = True
                
            if self.valor <= 0 or self.banderaP == False and self.lugar == 'NivelP':
                print(f'distancia {self.distancia}')
                print('bomba apagada')
                GPIO.output(GPIO_PIN,GPIO.LOW)
                self.valor = False
            
            if self.distanciaS <= self.peticionLlenadoS and self.peticionLlenadoS and self.lugar == 'NIvelS' :
                print(f'distancia {self.distancia}')
                print('bomba encendida')
                GPIO.output(GPIO_PIN,GPIO.HIGH)
                self.valor = True
                
            else:
                print(f'distancia {self.distancia}')
                print('bomba pagada')
                GPIO.output(GPIO_PIN,GPIO.LOW)
                self.valor = False
        except:
            print('Ocurrio algun error con el sensor')
        
        return {'id': self.idsen, 'tipodedato': self.tipoDato, 'valor': self.valor, 'fecha': fecha_hora}


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



#GPIO.cleanup()
