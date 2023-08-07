from __future__ import annotations

import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("DOGECHIA_ROOT", "~/.dogechia/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("DOGECHIA_KEYS_ROOT", "~/.dogechia_keys"))).resolve()

SIMULATOR_ROOT_PATH = Path(os.path.expanduser(os.getenv("DOGECHIA_SIMULATOR_ROOT", "~/.dogechia/simulator"))).resolve()
