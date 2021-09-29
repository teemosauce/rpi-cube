from numpy.core.numeric import roll
from libs.effects.cube_effect import CubeEffect

import numpy as np
import random
import time


class CubeEffectA(CubeEffect):
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
      
        output = np.zeros((3, self.kx * self.ky * self.kz))
        for band in range(0, 7):
            for i in range(0, y_d[band]):
                front = self.get_position(band, 0, i)
                right = self.get_position(0, 7-band, i)
                left = self.get_position(7, band, i)
                back = self.get_position(7- band, 7, i)

                output[0][front] = 255
                output[1][front] = 0
                output[2][front] = 0

                output[0][right] = 0
                output[1][right] = 0
                output[2][right] = 255

                output[0][left] = 0
                output[1][left] = 255
                output[2][left] = 0

                output[0][back] = 255
                output[1][back] = 255
                output[2][back] = 0
        self.queue_output_array_noneblocking(output)