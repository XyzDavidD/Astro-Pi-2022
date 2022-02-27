
# Importing all the neccesary modules
from sense_hat import SenseHat
import time
import logging
import pandas as pd
from datetime import date 

sense = SenseHat()

# Declaring the vectors where we store data
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20041.12826888  .00000636  00000-0  19647-4 0  9996"
line2 =  "2 25544  51.6446 262.0895 0004888 248.3633 259.5861 15.49151660212163"
temp = []
hum = []
pres = []
tim = []
clock = []
clocktwo = []

# Time setup:
time_at_start = time.time()  # Time at start
max_time = 9500  # Maximum running time
delay_intre_afisari = 5  # Delay between showing data on the matrix

# Setting the color codes:
x = [0, 0, 0]  # Blank - for the flag
y = [255, 255, 0]  # Yellow - for the flag and text
b = [0, 0, 255]  # Blue - for the flag and text
r = [255, 0, 0]  # Red - for the flag
g = [0, 255, 0]  # Green - for some text
opb = [255, 255, 0] # Opposite of blue
bg = [255, 255, 255] # Background
txt = [200, 0, 230] # Text colour

# Creating the Romanian flag, the country were we come from!:)
def steag(nr_afisari, delay):
    """
    :param nr_afisari: How many times should the flag wave
    :param delay: Delay between the waves
    This function shows the flag right at the begggining.
    """
    stg_sus = [r, r, r, x, x, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               x, x, x, y, y, x, x, x]

    stg_jos = [x, x, x, y, y, x, x, x,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, x, x, b, b, b]

    # Animation
    j = 0  # Lines
    brk = 0  # Counter

    while brk < 8:
        sense.set_pixel(0, j, r)
        sense.set_pixel(1, j, r)
        sense.set_pixel(2, j, r)
        sense.set_pixel(3, j, y)
        sense.set_pixel(4, j, y)
        sense.set_pixel(5, j, b)
        sense.set_pixel(6, j, b)
        sense.set_pixel(7, j, b)

        j += 1
        brk += 1
        time.sleep(delay)

    time.sleep(delay)

    afisari = 0  # Moving flag
    while afisari < nr_afisari:
        afisari += 1
        sense.set_pixels(stg_jos)
        time.sleep(delay)
        sense.set_pixels(stg_sus)
        time.sleep(delay)

def get_show_data(scrl_spd, col_t, col_h, col_p, bk_t, bk_h, bk_p):
    """
    :param scrl_spd: Speed of the scrolling text
    :param col_t: Text colour for the temperature
    :param col_h: Text colour for the humidity
    :param col_p: Text colour for the pressure
    :param bk_t: Background colour for the temperature
    :param bk_h: Background colour for the humidity
    :param bk_p: Background colour for the pressure
       This is our function for collecting the data from the sensors,
    and also showing it on the LED Matrix.
    """
    # Setting the date
    t5 = time.localtime().tm_hour
    t6 = time.localtime().tm_min
    timp = date.today()
    t1 = round(sense.get_temperature_from_humidity())
    t2 = round(sense.get_temperature_from_pressure())
    t3 = int((t1 + t2) / 2)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())

    # Showing it on the Sense Hat LEDs
    sense.show_message("Temperature=" + str(t3) + "C", scroll_speed=scrl_spd, text_colour=col_t, back_colour=bk_t)
    sense.show_message("Humidity=" + str(h) + "%", scroll_speed=scrl_spd, text_colour=col_h, back_colour=bk_h)
    sense.show_message("Pressure=" + str(p) + "hPa", scroll_speed=scrl_spd, text_colour=col_p, back_colour=bk_p)
    
    # And clearing the Sense Hat LEDs
    sense.clear()
    

def logger():
    """
        This function is saving the relevant data in the data01.csv file
    and it also gets the height of the ISS. 
    """
    # Sensors:
    t5 = time.localtime().tm_hour
    t6 = time.localtime().tm_min
    timp = date.today()
    t1 = round(sense.get_temperature_from_humidity())
    t2 = round(sense.get_temperature_from_pressure())
    t3 = int((t1 + t2) / 2)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())

    # Adding values from the sensor to the vectors
    temp.append(t3)
    clock.append(t5)
    clocktwo.append(t6)
    hum.append(h)
    pres.append(p)
    tim.append(timp)

    dict =  {
        'Day' : tim,
        'Clock Time Hours' : clock,
        'Clock Time Minutes' : clocktwo,
        'Temperature' : temp,
        'Pressure' : pres,
        'Humidity' : hum
    }
    df = pd.DataFrame(dict)
    df.to_csv('Chart.csv')

# Running the program 

steag(3, 0.5)  # Lowering of the flag

while (time.time() - time_at_start - delay_intre_afisari - 10) < max_time:
    
    get_show_data(0.1, txt, txt, txt, bg, bg, bg)
    
    logger()
    
    time.sleep(delay_intre_afisari)
