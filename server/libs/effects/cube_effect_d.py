from numpy.core.numeric import roll
from libs.effects.cube_effect import CubeEffect

import numpy as np
import random
import time


class CubeEffectD(CubeEffect):
    def run(self):
        effect_config = self.get_effect_config("effect_power")
        led_count = self._device.device_config["led_count"]
        n_fft_bins = self._config["general_settings"]["n_fft_bins"]
        led_mid = self._device.device_config["led_mid"]

        audio_data = self.get_audio_data()
        y = self.get_mel(audio_data)

        if y is None:
            return

        y_max = np.max(y)
        if y_max > 0: 
            y_d = y * 8 / y_max
        else:
            y_d = y

        self.no_voice = (y_max == 0)

        y_d = y_d.astype(int)
        if y is None:
            return
      
        output = self.shift(axis=0, direction=-1)

        for band in range(0, 8):

            if not self.no_voice:
                rand_num = random.randint(0, 3)
                
                for i in range(rand_num):
                    rand_x = random.randint(0, 7)
                    rand_y = random.randint(0, 7)
                    n = self.get_position(rand_x, rand_y, 7)
                    output[0][n] = 255
                    output[1][n] = 0
                    output[2][n] = 0

        self.queue_output_array_noneblocking(output)
        self.prev_output = output