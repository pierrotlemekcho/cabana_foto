#!/usr/bin/env python
import serial
import datetime

def faire_trame(f):
    print f 
# essai de pour git
  
if __name__ == '__main__' :
    s = serial.Serial(port='/dev/ttyAMA0', baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)
    carac = None
    ligne = ''
    trame = {}
    while carac != '\x03' : 
        carac = s.read(1) # attendre une fin de trame
        while True :
            carac = s.read(1)
            if carac == '\x03' : #fin de de trame ,---> trame en traitement
	        date = str(datetime.datetime.now())
	        trame['date'] = date
                faire_trame(trame)
            elif carac == '\x02': # debut trame on reinitialise la trame
                trame = {}
            elif carac == '\n' :#debut ligne on reinitialise la ligne
                ligne = ''
            elif carac == '\r' :#fin de ligne traitement donne
                try :
                    label, valeur, verif = ligne.split()
                except ValueError :
                    continue
                verif = ord(verif)
                calcul = (sum(bytearray(label+' '+valeur)) & 0x3f ) + 0x20
                if verif == calcul : # ligne valide donc prendre en compte
                    trame[label] = valeur
            else:
                ligne = ligne + carac
