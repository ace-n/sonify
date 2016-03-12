# https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file

import time, pyaudio, wave, sys
import numpy as np

# length of data to read.
chunk = 1024
wfs = []
wf = None
wf_index = 0
next_time = 0.
blend_data = None

def play(files):
    global wf, next_time, blend_data
    blend_data = None

    wfs = []
    for file in files:
	wfs.append(wave.open(file, 'rb'))

    p = pyaudio.PyAudio()
    wf0 = wfs[0]
    wf = wfs[0]
    wf_index = 0

    def callback(in_data, frame_count, time_info, status):
        global wf, wf_index, next_time, blend_data

        if next_time < 1.:
		next_time = time_info["output_buffer_dac_time"]
        cur_time = time_info["current_time"]

        data = wf.readframes(frame_count)
        if cur_time + 0.002 > next_time:
            next_time = 0.
            wf_index += 1
            if wf_index < len(wfs):
                wf = wfs[wf_index]
                blend_data = data

        if blend_data is not None:
            #data = data + blend_data
            blend_data = None
            print data
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf0.getsampwidth()),
                 channels=wf0.getnchannels(),
                 rate=wf0.getframerate(),
                 output=True,
                 stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.05)

    stream.stop_stream()
    stream.close()
    p.terminate()

def play_old(files):
    wfs = []
    for file in files:
	wfs.append(wave.open(file, 'rb'))

    p = pyaudio.PyAudio()
    wf0 = wfs[0]

    for wf in wfs:

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf0.getsampwidth()),
                 channels=wf0.getnchannels(),
                 rate=wf0.getframerate(),
                 output=True,
                 stream_callback=callback)

        stream.start_stream()


        time.sleep(0.05)

        wf.close()

        stream.stop_stream()
        stream.close()
    p.terminate()
