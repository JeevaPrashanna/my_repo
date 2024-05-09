import time
import serial
import numpy as np

# added new line of code
import pandas as pd

from cmath import exp,pi
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

input_=1
while 1 :
    input_ = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input_ + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print(">>" + out)


def fft(out):
        N=len(out)
        if N<=1:
            return out
        #division
        even=fft(out[0::2])
        odd=fft(out[1::2])
        # storing the combinations of results
        temp=np.zeros(N).astype(np.complex64)
        for u in range(N//2):
            temp[u]=even[u]+exp(-2j* pi *u/N)*odd[u]
            temp[u+N//2]=even[u]-exp(-2j* pi *u/N)*odd[u]
            return temp
F_fft=fft([0, 1, 2, 3])
print(F_fft)
