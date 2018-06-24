import picamera
from PIL import Image
import RPi.GPIO as GPIO
import time
import cups

""" Prend des photo ,redimensionne,archive ,imprime

BOUTON --> GPIO 23 contact par poussoir 
"""
LED_V = 17
LED_J = 4
BOUTON = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_J, GPIO.OUT)
GPIO.setup(LED_V, GPIO.OUT)
GPIO.setup(BOUTON, GPIO.IN)

GPIO.output(LED_J, GPIO.LOW)
GPIO.output(LED_V, GPIO.HIGH)

ETAT_BOUTON = False
I=0
conn = cups.Connection ()
cadre = 'cadre_shim600.png'
im4 =Image.open(cadre)

with  picamera.PiCamera() as camera:
    resolution1 = 2592 , 1458
    camera.resolution = (resolution1)
    camera.start_preview()
    
    while True :
        Lecture1 = GPIO.input(BOUTON)
        ETAT1 = not(Lecture1)
        if ( ETAT1 != ETAT_BOUTON):
            time.sleep(.01)
            Lecture2 = GPIO.input(BOUTON)
            ETAT2 = not(Lecture2)
            if ( ETAT1 == ETAT2):
                ETAT_BOUTON = ETAT2

        if (ETAT_BOUTON == True) :
            #print('BP ouvert ')
            GPIO.output(LED_J, GPIO.LOW)
            GPIO.output(LED_V, GPIO.HIGH)
        else :
            I=I+1
            #print ('BP pousser')
            GPIO.output(LED_J, GPIO.HIGH)
            GPIO.output(LED_V, GPIO.LOW)
            
            h = time.strftime("%y%m%d%H%M%S")
            ficphoto1png = '/media/disk1/photo'+h+'.png'
            ficphoto1_reduc_png = '/media/disk1/photo_reduc'+h+'.png'
            fotomaton = '/media/disk1/fotomaton '+h+'.png'
            time.sleep(1)
            camera.capture(ficphoto1png)
            im1 = Image.open(ficphoto1png)
            im2 = im1.resize((2012,1128))
            im4 =Image.open(cadre)
            im4.paste(im2,(116,72))
            im4.paste(im2 ,(116,1484))
            im4.save(fotomaton ,'PNG')
            retour = conn.printFile("Canon_iP2800_series",fotomaton,"Hello",{})
            while conn.getJobAttributes(retour)["job-state"] != 9 :
                pass

#            if I > 2 :
#                break
                            
GPIO.cleanup()
