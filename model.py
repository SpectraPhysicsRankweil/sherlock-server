from typing import List, Dict
import time


class Device:
    def __init__(self, ip_list: List[str], hostname: str, unique_id: str = None):
        self.ip_list = ip_list
        self.hostname = hostname
        self.unique_id = unique_id

        self.first_timestamp = time.time()
        self.last_timestamp = self.first_timestamp

    def update_timestamp(self):
        self.last_timestamp = time.time()


class Network:
    def __init__(self, remote_ip: str):
        self._remote_ip = remote_ip
        self._devices = dict()  # type: Dict[str, Device]

    def __contains__(self, unqiue_key):
        return unqiue_key in self._devices

    def __getitem__(self, unique_id):
        return self._devices[unique_id]

    def __setitem__(self, unique_id, device):
        self._devices[unique_id] = device

    @property
    def remote_ip(self):
        return self._remote_ip

    @property
    def devices(self):
        return tuple(self._devices.values())


networks = dict()  # type: Dict[str, Network]
