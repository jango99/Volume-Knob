# CircuitPython AnalogIn Demo
import time
import board
import math
from analogio import AnalogIn
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

analog_in1 = AnalogIn(board.A1)  # pin 2
analog_in2 = AnalogIn(board.A3)  # pin 3
cc = ConsumerControl()

# Converts the value to a valid voltage
def get_voltage(pin):
    return (pin.value * 3.3) / 65536
# Algorithm meant to find the volume level according to volume knob on first startup
def find_volume(v_level):
    count = 0
    check_decrease = False
    while(count < 50 and check_decrease == False):  # sets volume to 0
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        count = count + 1
    check_decrease = True

    level = 0
    check_increase = False
    while (level < (v_level/2) and check_increase == False):
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        level = level + 1
    check_increase = True

def get_volume(vk_voltage):
    return math.floor((vk_voltage*100 / 3.25) / 2)*2

def change_volume(p_v, c_v):
    if (p_v > c_v):
        while (p_v > c_v):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            p_v = p_v - 2

    if (p_v < c_v):
        while (p_v < c_v):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            p_v = p_v + 2


# changes the volume to the one according to the volume knob on first setup
find_volume(get_volume(get_voltage(analog_in1)))
past_volume = get_volume(get_voltage(analog_in1))
while True:
    #print(get_volume(get_voltage(analog_in1)),) # Prints out the voltage from pin 2 (volume knob)
    current_volume = get_volume(get_voltage(analog_in1))
    #print("past volume: ", past_volume, "current volume: ", current_volume)
    #print (past_volume)
    change_volume(past_volume, current_volume)
    time.sleep(0.01)
    past_volume = current_volume
    #print((120*get_voltage(analog_in2),))  # prints out the voltage from pin 3 (pause/unpause switch)
    # Play/pauses song
    if (get_voltage(analog_in2)*120 > 1):
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        time.sleep(0.2)