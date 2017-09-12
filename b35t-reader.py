#!/usr/bin/env python 

import pexpect
import time
import sys

# Fill in the MAC address for your device here
# Find the MAC address of the B35T by running `sudo hcitool lescan`
# and looking for '<MAC ADDRESS> BDM'
DEVICE_MAC = '50:8C:B1:70:7B:50'

# Connect to the device.
def connectToDevice(child, mac):
    try:
        print("Connecting to"),
        print(mac),
        child.sendline("connect {0}".format(mac))
        child.expect("Connection successful", timeout=5)
        print("Connected!")
    except pexpect.exceptions.TIMEOUT:
        print("Failed!")

# function to transform hex byte like "0a" into unsigned integer
#def hexStrToByte(hexstr):
#    val = int(hexstr[0:2],16)
#    return val

# function to transform hex string like "0a cd" into signed integer
#def hexStrToInt(hexstr):
#    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
#    if ((val&0x8000)==0x8000): # treat signed 16bits
#        val = -((val^0xffff)+1)
#    return val

print("Using B35T address:"),
print(DEVICE_MAC)

# Run gatttool interactively.
print("Running gatttool...")
childProc = pexpect.spawn("gatttool -I")
connectToDevice(childProc, DEVICE_MAC)
#timeoutCounter = 0

# loop forever reading data lines
while True:
    try:
        childProc.expect("Notification handle = 0x002e value: ", timeout=2)
        childProc.expect("\r\n", timeout=2)
        data = childProc.before.split(' ')
        #print("Raw data:"),
        #print(data)
        sign = int(data[0],16)

        # sign char must be + or -, ignore others for now
        if sign != 43 and sign != 45:
            continue

        digit_a = int(data[1],16)
        digit_b = int(data[2],16)
        digit_c = int(data[3],16)
        digit_d = int(data[4],16)
        decimalPos = int(data[6],16)
        digitStr = ''

        if digit_a == 63 and digit_d == 63: # check for overload
            digitStr += '  0.L '
        else:
            if sign == 45:
                digitStr += '-'
            else:
                digitStr += ' '
            digitStr += chr(digit_a)
            if decimalPos == 49:
                digitStr += '.'
            digitStr += chr(digit_b)
            if decimalPos == 50:
                digitStr += '.'
            digitStr += chr(digit_c)
            if decimalPos == 52:
                digitStr += '.'
            digitStr += chr(digit_d)

        units_a = int(data[9],16)
        units_b = int(data[10],16)
        if units_a == 64 and units_b == 128:
            unitsStr = 'mV'
        elif units_a == 0 and units_b == 128:
            unitsStr = 'V'
        elif units_a == 0 and units_b == 32:
            unitsStr = 'Ohm'
        elif units_a == 32 and units_b == 32:
            unitsStr = 'KOhm'
        elif units_a == 16 and units_b == 32:
            unitsStr = 'MOhm'
        elif units_a == 0 and units_b == 64:
            unitsStr = 'A'
        elif units_a == 64 and units_b == 64:
            unitsStr = 'mA'
        elif units_a == 128 and units_b == 64:
            unitsStr = 'uA'
        elif units_a == 0 and units_b == 2:
            unitsStr = 'Celsius'
        elif units_a == 0 and units_b == 1:
            unitsStr = 'Fahrenheit'
        elif units_a == 0 and units_b == 8:
            unitsStr = 'Hz'
        elif units_a == 2 and units_b == 0:
            unitsStr = '%'
        elif units_a == 0 and units_b == 16:
            unitsStr = 'hFE'
        elif units_a == 4 and units_b == 128:
            unitsStr = 'V-diode'
        elif units_a == 0 and units_b == 4:
            unitsStr = 'nF'
        elif units_a == 8 and units_b == 32:
            unitsStr = 'Ohm-continuity'
        else:
            print("unknown units code (%d,%d)" % (units_a, units_b))
            unitsStr = ''

        mode  = int(data[7],16)

        if mode == 0:
            modeStr = ''
        elif mode == 1:
            modeStr = '(Ohm-manual)'
        elif mode == 8:
            modeStr = '(AC-minmax)'
        elif mode == 9:
            modeStr = '(AC-manual)'
        elif mode == 16:
            modeStr = '(DC-minmax)'
        elif mode == 17:
            modeStr = '(DC-manual)'
        elif mode == 20:
            modeStr = '(delta)'
        elif mode == 32:
            # this is hz, no ranging.
            modeStr = ''
        elif mode == 33:
            modeStr = '(Ohm-auto)'
        elif mode == 41:
            modeStr = '(AC-auto)'
        elif mode == 49:
            modeStr = '(DC-auto)'
        elif mode == 51:
            modeStr = '[HOLD]'
        else:
            modeStr = "<unknown mode "+str(mode)+">"

        print(digitStr),
        print(unitsStr),
        print(modeStr)

    except pexpect.exceptions.TIMEOUT:
        print("Timeout waiting for data")
        print("Reconnecting...")
        connectToDevice(childProc, DEVICE_MAC)
    except KeyboardInterrupt:
        sys.exit()
