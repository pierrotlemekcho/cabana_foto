import picamera
from PIL import Image
import RPi.GPIO as GPIO
import time
import cups

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
cadre = 'cadre_A6_300dpi.png'
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
            ficphoto1png = 'photo'+h+'.png'
            ficphoto1_reduc_png = 'photo_reduc'+h+'.png'
            fotomaton = 'fotomaton '+h+'.png'
            time.sleep(1)
            camera.capture(ficphoto1png,resize=(1122,631))
            im1 = Image.open(ficphoto1png)
            im4 =Image.open(cadre)
            im4.paste(im1,(59,59))
            im4.paste(im1 ,(59,933))
            im4.save(fotomaton ,'PNG')
            retour = conn.printFile("Canon_iP4800_series",fotomaton,"Hello",{})
            while conn.getJobAttributes(retour)["job-state"] != 9 :
                pass

            if I > 2 :
                break
                            
GPIO.cleanup()
