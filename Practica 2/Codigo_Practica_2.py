import RPi.GPIO as GPIO
from time import sleep
import I2C_LCD_driver
import threading
import spidev
from datetime import datetime
import time
import Adafruit_DHT

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

delay = 1
buzzer = 12  # GPIO26
GPIO.setup(buzzer, GPIO.OUT)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Define GPIO to Keyboard
ky_A = 32  # GPIO13
ky_porcentaje = 36  # GPIO19
ky_uno = 38  # GPIO20
ky_enter = 40  # GPIO21
led = 15  
fuego=11 
luz = 13
led_luz = 10

motor = 8
lcd_rows = 2

Password = 'A%1'
Password_comparar = ''
pattern_set = False  # Variable para comprobar si el patrón está siendo ingresado
failed_attempts = 0  # Contador de intentos fallidos

# Obtener la fecha y hora actual
now = datetime.now()

# Setup
GPIO.setup(ky_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_porcentaje, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_uno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_enter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(fuego,GPIO.IN)
GPIO.setup(motor,GPIO.OUT)
GPIO.setup(luz,GPIO.IN)
GPIO.setup(led_luz,GPIO.OUT)
GPIO.output(led, GPIO.LOW)
GPIO.output(motor, GPIO.LOW)
GPIO.output(led_luz, GPIO.LOW)

# mylcd = RPi_I2C_driver.lcd()
# mylcd.backlight(0)
# mylcd.lcd_clear()

def bloquear_entrada(tiempo_bloqueo):
    """Bloquea la entrada de patrones por un tiempo determinado."""
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Intentos fallidos", 1)
    mylcd.lcd_display_string("Espere 15 seg", 2)
    sleep(1)
    for i in range(tiempo_bloqueo, 0, -1):
        mylcd.lcd_clear()
        print(f"Bloqueado por {i} segundos")
        mylcd.lcd_display_string("Bloqueado por", 1)
        mylcd.lcd_display_string(str(i)+" segundos", 2)
        sleep(1)
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Pruebe de", 1)
    mylcd.lcd_display_string("Nuevo", 2)
    sleep(1)

def check_password_input():
    global Password_comparar, pattern_set, failed_attempts
    while True:
        if GPIO.input(ky_enter) == GPIO.HIGH and not pattern_set:
            pattern_set = True
            Password_comparar = ''
            # mylcd.lcd_clear()
            # mylcd.lcd_display_string("Ingrese Patron:", 1)
            # mylcd.lcd_display_string("***", 2)
            print("Ingrese Patron:")
            mylcd.lcd_display_string("Ingrese el patron", 1)
            mylcd.lcd_display_string("patron", 2)
            sleep(0.5)
        elif pattern_set:
            if GPIO.input(ky_A) == GPIO.HIGH:
                Password_comparar += 'A'
                # mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                print('*' * len(Password_comparar))
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Contra", 1)
                mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                sleep(0.5)
            elif GPIO.input(ky_porcentaje) == GPIO.HIGH:
                Password_comparar += '%'
                # mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                print('*' * len(Password_comparar))
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Contra", 1)
                mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                sleep(0.5)
            elif GPIO.input(ky_uno) == GPIO.HIGH:
                Password_comparar += '1'
                # mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                print('*' * len(Password_comparar))
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Contra", 1)
                mylcd.lcd_display_string('*' * len(Password_comparar), 2)
                sleep(0.5)
            elif GPIO.input(ky_enter) == GPIO.HIGH:
                print("tecla presionada Enter")
                if Password_comparar == Password:
                    # mylcd.lcd_clear()
                    # mylcd.lcd_display_string("Bienvenido", 1)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Contra", 1)
                    mylcd.lcd_display_string("Correcta", 2)
                    print("Contrasenia correcta")
                    GPIO.output(led, GPIO.HIGH)
                    sleep(1)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Bienvenido", 1)
                    sleep(2)
                    mylcd.lcd_clear()
                    pattern_set = False
                    Password_comparar = ''
                    failed_attempts = 0  # Reinicia los intentos fallidos
                    sleep(0.5)
                    return True
                else:
                    failed_attempts += 1
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Intento fallido: ", 1)
                    mylcd.lcd_display_string(str(failed_attempts), 2)
                    sleep(1)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Contra", 1)
                    mylcd.lcd_display_string("Incorrecta", 2)
                    sleep(1)
                    mylcd.lcd_clear()
                    mylcd.lcd_display_string("Pruebe de", 1)
                    mylcd.lcd_display_string("Nuevo", 2)
                    sleep(1)
                    mylcd.lcd_clear()
                    print(f"Intentos fallidos: {failed_attempts}")
                    print("Contrasenia incorrecta")
                    # mylcd.lcd_clear()
                    # mylcd.lcd_display_string("Patron", 1)
                    # mylcd.lcd_display_string("Incorrecto", 2)
                    pattern_set = False
                    GPIO.output(led, GPIO.LOW)
                    Password_comparar = ''
                    sleep(0.5)
                    if failed_attempts >= 3:
                        bloquear_entrada(15)  # Bloquea el sistema por 15 segundos
                        failed_attempts = 0  # Reinicia los intentos fallidos
                    return False

def sensor_fuego():
    if(GPIO.input(fuego)==0):
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Fuego Detectado", 1)
        # mylcd.lcd_display_string("Motor Encendido", 2)
        sleep(1)
        mylcd.lcd_clear()
        print("Se esta quemando")
        GPIO.output(buzzer,GPIO.HIGH)
    else:
        print("Todo Normal")
        GPIO.output(buzzer,GPIO.LOW)

def sensor_luz():
    if(GPIO.input(luz)==0):
        print("Luz detectada.")
        GPIO.output(led_luz,GPIO.LOW)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Luces Apagadas", 1)
        sleep(1)
        mylcd.lcd_clear()
        # mylcd.lcd_display_string("Motor Encendido", 2)
    else:
        print("No hay luz. Encendiendo leds")
        GPIO.output(led_luz,GPIO.HIGH)

def sensor_temp():
    humidity, temperature = Adafruit_DHT.read_retry(11,4)
    if humidity is not None and temperature is not None:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Temp={0:0.1f}C".format(temperature))
        mylcd.lcd_display_string(f"{str(now.day)}/{str(now.month)}/{str(now.year)}", 2)
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        GPIO.output(motor,GPIO.HIGH)
        sleep(2)
        GPIO.output(motor,GPIO.LOW)
        # if (temperature>=20):
        #     GPIO.output(motor,GPIO.HIGH)
        # else:
        #     GPIO.output(motor,GPIO.LOW)
    else:
        print("Sensor failure. Check wiring.")


print("Programa iniciado")
GPIO.output(buzzer,GPIO.LOW)
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
sleep(2)

# Verificar la contraseña y ejecutar el bucle principal si es correcta
while not check_password_input():
    print("Repetir")
    continue

mylcd.lcd_clear()
mylcd.lcd_display_string(f"{str(now.day)}/{str(now.month)}/{str(now.year)}", 2)
try:
    while True:
        sleep(1) 
        sensor_fuego()#Funcion de Sensor de Fuego 
        sensor_luz() # Funcion de sensor de luz
        sensor_temp() #Funcion de sensor temperatura

except KeyboardInterrupt:
    mylcd.lcd_clear()
    GPIO.cleanup()

