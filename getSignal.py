import pyaudio
import numpy

RATE = 16000
RECORD_SECONDS = 5 
CHUNKSIZE = 1024


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)

frames = []
for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
    data = stream.read(CHUNKSIZE)
    frames.append(numpy.fromstring(data, dtype=numpy.int16))


numpydata = numpy.hstack(frames)
# numpy.savetxt('signal.csv', numpydata[None], fmt='%d',newline=',', delimiter=',')
numpy.savetxt('signal.csv', numpydata,fmt='%d', newline='\n', header='data')

# close stream
stream.stop_stream()
stream.close()
p.terminate()