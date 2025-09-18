import RPi.GPIO as GPIO
from time import sleep
import pio
import Ports
import threading
import spidev
from datetime import datetime


# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pio.uart = Ports.UART()

delay = 1
buzzer = 37 #GPIO26
GPIO.setup(buzzer, GPIO.OUT)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

# Definir los pines
LDR_PIN = 29  # GPIO5
LED_PIN = 31  # GPIO6
FLAME_PIN = 11  # GPIO17
AIR_PIN = 36  # GPIO16

# Define GPIO to LCD mapping (using BOARD numbering)
LCD_RS = 26  # GPIO7
LCD_E = 13  # GPIO27
LCD_D4 = 22  # GPIO25
LCD_D5 = 18  # GPIO24
LCD_D6 = 16  # GPIO23
LCD_D7 = 12  # GPIO18

#agregre esto---------
gas_Sensor = 15  # Cambié 18 por 15
red_light = 32  # Cambié 31 por 32
Buzzer = 37  # Cambié 29 por 26

GPIO.setup(gas_Sensor, GPIO.IN)  # DB7
GPIO.setup(red_light, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)
#---------------------------------------

# Define GPIO to Keyboard
ky_A = 33  # GPIO13
ky_porcentaje = 35  # GPIO19
ky_uno = 38  # GPIO20
ky_enter = 40  # GPIO21
led = 7  # GPIO4

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

Password = 'A%1'
Password_comparar = ''
temp_channel = 0
# Obtener la fecha y hora actual
now = datetime.now()

GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT)  # RS
GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(FLAME_PIN, GPIO.IN)
# Setup
GPIO.setup(ky_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_porcentaje, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_uno, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ky_enter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(AIR_PIN, GPIO.OUT)

def check_password_input():
    global Password_comparar
    while True:
        if GPIO.input(ky_A) == GPIO.HIGH:
            Password_comparar += 'A'
            pio.uart.println("tecla presionada A")
            sleep(0.05)
        elif GPIO.input(ky_porcentaje) == GPIO.HIGH:
            Password_comparar += '%'
            pio.uart.println("tecla presionada %")
            sleep(0.05)
        elif GPIO.input(ky_uno) == GPIO.HIGH:
            Password_comparar += '1'
            pio.uart.println("tecla presionada 1")
            sleep(0.05)

        if GPIO.input(ky_enter) == GPIO.HIGH:
            pio.uart.println("tecla presionada Enter")
            if Password_comparar == Password:
                lcd_string("Bienvenido", LCD_LINE_1)
                lcd_string("", LCD_LINE_2)
                pio.uart.println("Contrasenia correcta")
                GPIO.output(led, GPIO.HIGH)
                Password_comparar = ''
                sleep(0.05)
                GPIO.cleanup()
            else:
                Password_comparar = ''
                pio.uart.println("Contrasenia incorrecta")
                lcd_string("Contrasenia", LCD_LINE_1)
                lcd_string("incorrecta", LCD_LINE_2)
                GPIO.output(led, GPIO.LOW)
                sleep(0.05)
                GPIO.cleanup()
            return True
        return False

def check_sensors():
    sensor_triggered = False
    while True:
        # Leer el valor del LDR
        if GPIO.input(LDR_PIN) == GPIO.LOW:
            # Suficiente luz detectada, apagar el LED
            GPIO.output(LED_PIN, GPIO.LOW)
            sensor_triggered = True
        else:
            # Poca luz detectada, encender el LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            sensor_triggered = True
        # Detección de fuego
        if GPIO.input(FLAME_PIN) == GPIO.HIGH:
            pio.uart.println("fuego detectado")
            sensor_triggered = True
            sleep(0.5)
        else:
            # pio.uart.println("no hay fuego")
            sensor_triggered = True

        if GPIO.input(gas_Sensor):
            pio.uart.println("Gas Detectado")
            GPIO.output(Buzzer, True)
            GPIO.output(red_light, True)  
            sensor_triggered = True
            sleep(0.5)

        else:
            sensor_triggered = True
            GPIO.output(Buzzer, False)
            GPIO.output(red_light, False)

        return sensor_triggered

def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to calculate temperature from TMP36 data, rounded to specified number of decimal places.
def ConvertTemp(data, places):
    # ADC Value
    # (approx)  Temp  Volts
    #    0      -50    0.00
    #   78      -25    0.25
    #  155        0    0.50
    #  233       25    0.75
    #  310       50    1.00
    #  465      100    1.50
    #  775      200    2.50
    # 1023      280    3.30

    temp = ((data * 330) / float(1023))
    temp = round(temp, places)
    return temp

def chek_sensor_temp():
    GPIO.cleanup()
    while True:
        temp_level = ReadChannel(temp_channel)
        temp = ConvertTemp(temp_level, 2)
        if temp >= 27:
            GPIO.output(AIR_PIN, GPIO.HIGH)
            lcd_string(f"{str(temp)}", LCD_LINE_1)
            lcd_string(f"{str(now.day)}/{str(now.month)}/{str(now.year)}", LCD_LINE_2)
            sleep(0.5)
            GPIO.cleanup()
        else:
            GPIO.output(AIR_PIN, GPIO.LOW)
            lcd_string(f"{str(temp)}", LCD_LINE_1)
            lcd_string(f"{str(now.day)}/{str(now.month)}/{str(now.year)}", LCD_LINE_2)
            sleep(0.5)
            GPIO.cleanup()

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On, Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Inicializa el LCD
lcd_init()

# Inicia los hilos
# check_password_thread = threading.Thread(target=check_password_input)
# check_password_thread.start()

# check_sensors_thread = threading.Thread(target=check_sensors)
# check_sensors_thread.start()

check_sensor_temp_thread = threading.Thread(target=chek_sensor_temp)
check_sensor_temp_thread.start()

# Bucle principal
try:
    while True:
        sleep(0.5)  # Esperar 0.5 segundos en cada iteración
        if check_password_input():
            GPIO.cleanup()
            continue
        if check_sensors():
            GPIO.cleanup()
            continue

except KeyboardInterrupt:
    GPIO.cleanup()
    pio.uart.println("Programa terminado.")