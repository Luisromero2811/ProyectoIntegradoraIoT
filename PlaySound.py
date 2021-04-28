import gtts
import playsound
import time


class AudioPython:

    def playsound_pila_llena(self, valor):
        sound = gtts.gTTS('La pila esta llena al ' + str(valor) + '%', lang='es-us')
        sound.save('audio_pila_llena.mp3')
        playsound.playsound('audio_pila_llena.mp3')

    def playsound_pila_vacia(self):
        sound = gtts.gTTS('La pila esta vacia', lang='es-us')
        sound.save('audio_pila_vacia.mp3')
        playsound.playsound('audio_pila_vacia.mp3')

    def playsound_suelo_humedo(self, valor):
        sound = gtts.gTTS('El suelo esta humedo al ' + str(valor) + '%', lang='es-us')
        sound.save('audio_suelo_humedo.mp3')
        playsound.playsound('audio_suelo_humedo.mp3')

    def playsound_suelo_seco(self):
        sound = gtts.gTTS('El suelo es seco', lang='es-us')
        sound.save('audio_suelo_seco.mp3')
        playsound.playsound('audio_suelo_seco.mp3')
    
    def playsound_move_detectado(self):
        sound = gtts.gTTS('Se ha detectado movimiento', lang='es-us')
        sound.save('audio_move_detectado.mp3')
        playsound.playsound('audio_move_detectado.mp3')