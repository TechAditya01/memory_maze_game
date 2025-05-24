import wave
import struct
import math

def create_tone(filename, duration=0.5, freqs=[440, 660], volume=16000):
    framerate = 44100
    nframes = int(duration * framerate)
    comptype = "NONE"
    compname = "not compressed"
    nchannels = 1
    sampwidth = 2

    wav_file = wave.open(filename, 'w')
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

    for i in range(nframes):
        value = 0
        for freq in freqs:
            value += int(volume * math.sin(2 * math.pi * freq * i / framerate))
        value = int(value / len(freqs))
        data = struct.pack('<h', value)
        wav_file.writeframesraw(data)

    wav_file.close()

# Pleasant win sound: two-tone harmony
create_tone('win.wav', freqs=[660, 880])

# Pleasant lose sound: slower, minor tone
create_tone('lose.wav', freqs=[330, 220], duration=0.7)
