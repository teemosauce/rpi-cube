import time
import pyaudio
import wave
import numpy as np
from libs.dsp import DSP

# 
def play_audio_file(fname='/home/pi/Desktop/music_led_strip_control/server/test.wav'):
    wf = wave.open(fname, 'rb')
    audio = pyaudio.PyAudio()
    print('nframes', wf.getnframes())
    print('framerate', wf.getframerate())
    print('sampwidth', wf.getsampwidth(), audio.get_format_from_width(wf.getsampwidth()))
    print('nchannels', wf.getnchannels())
    
    # audio.terminate()
    frames_per_buffer = 512

    # print('get_device_count', audio.get_device_count())
    # print('0', audio.get_device_info_by_host_api_device_index(0, 0))
    # print('1', audio.get_device_info_by_host_api_device_index(0, 1))
    # print('2', audio.get_device_info_by_host_api_device_index(0, 2))
    # print('3', audio.get_device_info_by_host_api_device_index(0, 3))

    def callback(in_data, frame_count, time_info, status):
        
        # print(in_data)
        print(frame_count)
        print(time_info)
        data = wf.readframes(frame_count)
        print(len(data))
        return data, pyaudio.paContinue
       

    stream = audio.open(
        format=audio.get_format_from_width(wf.getsampwidth()),
        channels=1,
        rate=wf.getframerate(),
        input=False,
        output=True,
        output_device_index=0,
        frames_per_buffer=frames_per_buffer,
        stream_callback=callback
        )

    data = wf.readframes(frames_per_buffer)

    # print(len(data))

    try:
        stream.start_stream()
        # while data != b'':
        #     # print(data)
        #     # to_arr(data)
        #     stream.write(data)
        #     data = wf.readframes(frames_per_buffer)

        print('close')
        while stream.is_active():
            time.sleep(0.1)
        stream.stop_stream()
        stream.close()

        audio.terminate()
    except KeyboardInterrupt:
        print('throw KeyboardInterrupt')
        stream.stop_stream()
        stream.close()

        audio.terminate()


def to_arr(in_data):
    # Convert the raw string audio stream to an array.
    y = np.fromstring(in_data, dtype=np.int16)
    # Use the type float32.
    y = y.astype(np.float32)

    print(y.shape)
    # # Process the audio stream.
    # audio_datas = self._dsp.update(y)

    # # Check if value is higher than min value.
    # if audio_datas["vol"] < self._config["general_settings"]["min_volume_threshold"]:
    #     # Fill the array with zeros, to fade out the effect.
    #     audio_datas["mel"] = np.zeros(self.n_fft_bins)

    # self._audio_queue.put_none_blocking(audio_datas)

    # self.end_time_2 = time()

    # if time() - self.ten_seconds_counter_2 > 10:
    #     self.ten_seconds_counter_2 = time()
    #     time_dif = self.end_time_2 - self.start_time_2
    #     fps = 1 / time_dif
    #     self.logger.info(f"Routine | FPS: {fps:.2f}")

    # self.start_time_2 = time()

play_audio_file()