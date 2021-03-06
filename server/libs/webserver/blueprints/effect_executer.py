from libs.webserver.executer_base import ExecuterBase


class EffectExecuter(ExecuterBase):

    # Return active effect.
    def get_active_effect(self, device):
        if device == self.all_devices_id:
            return self._config[self.all_devices_id]["effects"]["last_effect"]
        else:
            return self._config["device_configs"][device]["effects"]["last_effect"]

    def get_active_effects(self):
        devices = []
        for device_key in self._config["device_configs"]:
            current_device = dict()
            current_device["device"] = device_key
            current_device["effect"] = self._config["device_configs"][device_key]["effects"]["last_effect"]
            devices.append(current_device)
        return devices

    def set_active_effect(self, device, effect, for_all=False):
        if device == self.all_devices_id:
            self.set_active_effect_for_all(effect)
            return
        else:
            self._config["device_configs"][device]["effects"]["last_effect"] = effect
            self.save_config()

        self.put_into_effect_queue(device, effect, put_all=for_all)

    def set_active_effect_for_all(self, effect):
        self._config[self.all_devices_id]["effects"]["last_effect"] = effect
        self.save_config()
        self.refresh_device(self.all_devices_id)
        for device_key in self._config["device_configs"]:
            self.set_active_effect(device_key, effect, for_all=True)
