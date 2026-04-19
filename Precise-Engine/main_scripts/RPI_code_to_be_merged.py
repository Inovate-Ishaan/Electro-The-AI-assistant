import pyaudio
import numpy as np
import serial

# we now set the resolution and speed of sampling

CHUNK = 1024
RATE = 44100
sensitivity = 100
port_name = "/dev/ttyACM0"  # CHANGE ACCORDINGLY



p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


# we now set the serial connection to the arduino

ser = serial.Serial(port_name, 115200) 

while True:
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    fft_data = np.abs(np.fft.rfft(data))

    bass = int(np.mean(fft_data[0:10])/sensitivity)
    bass = min(255,bass)

    ser.write(bytes([bass]))