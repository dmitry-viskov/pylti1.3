import json
import os
from .dict import ToolConfDict


class ToolConfJsonFile(ToolConfDict):
    _configs_dir = None

    def __init__(self, config_file):
        if not os.path.isfile(config_file):
            raise Exception("LTI tool config file not found: " + config_file)
        self._configs_dir = os.path.dirname(config_file)

        cfg = open(config_file, 'r')
        iss_conf = json.loads(cfg.read())
        super(ToolConfJsonFile, self).__init__(iss_conf)
        cfg.close()

        for iss in iss_conf:
            private_key_file = iss_conf[iss]['private_key_file']
            if not private_key_file.startswith('/'):
                private_key_file = self._configs_dir + '/' + private_key_file

            prf = open(private_key_file, 'r')
            self.set_private_key(iss, prf.read())
            prf.close()
