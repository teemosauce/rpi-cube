from numpy.core.numeric import roll
from libs.effects.cube_effect import CubeEffect

import numpy as np
import random
import time


class CubeEffectC(CubeEffect):
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
        for band in range(0, 8):

            if 0 < y_d[band] <= 2:
                x1 = 3
                x2 = 4
            elif  2 < y_d[band] <= 4:
                x1 = 2
                x2 = 5
            elif  4 < y_d[band] <= 6:
                x1 = 1
                x2 = 6
            elif 6 < y_d[band]:
                x1 = 0
                x2 = 7
            else:
                x1 = -1
                x2 = -1
            y1 = x1
            y2 = x2

            if x1 != -1 and x2 != -1:
               output = self.box_wall(x1, y1, band, x2, y2, band, output)
        time.sleep(0.01)
               
        self.queue_output_array_noneblocking(output)
        self.prev_output = output

    def box_wall(self, x1, y1, z1, x2, y2, z2, output):
        for z in range(z1, z2 + 1):
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1): 
                    position = self.get_position(x, y, z)
                    output[0][position] = 0
                    output[1][position] = 255
                    output[2][position] = 0
        return output
    
