# %%
import pyaudio
# import matplotlib.pyplot as plt
# import numpy as np
import wave

# %%
# Initializing constants
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

# %%
# Stream object is initialized and opened to begin recording
pa = pyaudio.PyAudio()

# max_channels = pa.get_device_info_by_index(1)['maxInputChannels']  # Get the maximum input channels for device 0
# print("Max channels:", max_channels)
# CHANNELS = max_channels  # Use the maximum supported channels


print("Requirements: \n", pa.get_device_info_by_index(2))   


# Use the selected input device in your stream configuration
sample_size = pa.get_sample_size(FORMAT)

stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
    input_device_index=2
)
print("Start Recording...")

# %%
# setting the length of the recording
rec_time = 5
frames = []


for i in range(0, int(RATE/FRAMES_PER_BUFFER*rec_time)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

# Close all open streams since recording is completed
stream.stop_stream()
stream.close()
pa.terminate()


# %%
# Creating a new object to store the frames into a .wav file
obj = wave.open("creation1.wav", "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(pa.get_sample_size(FORMAT))
obj.setframerate(RATE)

# converting the frames list into a binary array and writing it to the audio object to be saved as a file
obj.writeframes(b"".join(frames)) 
obj.close()



