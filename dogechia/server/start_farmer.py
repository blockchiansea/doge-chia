from __future__ import annotations

import pathlib
import sys
from typing import Any, Dict, Optional

from dogechia.consensus.constants import ConsensusConstants
from dogechia.consensus.default_constants import DEFAULT_CONSTANTS
from dogechia.farmer.farmer import Farmer
from dogechia.farmer.farmer_api import FarmerAPI
from dogechia.rpc.farmer_rpc_api import FarmerRpcApi
from dogechia.server.outbound_message import NodeType
from dogechia.server.start_service import RpcInfo, Service, async_run
from dogechia.types.peer_info import UnresolvedPeerInfo
from dogechia.util.dogechia_logging import initialize_service_logging
from dogechia.util.config import load_config, load_config_cli
from dogechia.util.default_root import DEFAULT_ROOT_PATH
from dogechia.util.keychain import Keychain

# See: https://bugs.python.org/issue29288
"".encode("idna")

SERVICE_NAME = "farmer"


def create_farmer_service(
    root_path: pathlib.Path,
    config: Dict[str, Any],
    config_pool: Dict[str, Any],
    consensus_constants: ConsensusConstants,
    keychain: Optional[Keychain] = None,
    connect_to_daemon: bool = True,
) -> Service[Farmer]:
    service_config = config[SERVICE_NAME]

    fnp = service_config.get("full_node_peer")
    connect_peers = set() if fnp is None else {UnresolvedPeerInfo(fnp["host"], fnp["port"])}

    overrides = service_config["network_overrides"]["constants"][service_config["selected_network"]]
    updated_constants = consensus_constants.replace_str_to_bytes(**overrides)

    farmer = Farmer(
        root_path, service_config, config_pool, consensus_constants=updated_constants, local_keychain=keychain
    )
    peer_api = FarmerAPI(farmer)
    network_id = service_config["selected_network"]
    rpc_info: Optional[RpcInfo] = None
    if service_config["start_rpc_server"]:
        rpc_info = (FarmerRpcApi, service_config["rpc_port"])
    return Service(
        root_path=root_path,
        config=config,
        node=farmer,
        peer_api=peer_api,
        node_type=NodeType.FARMER,
        advertised_port=service_config["port"],
        service_name=SERVICE_NAME,
        connect_peers=connect_peers,
        on_connect_callback=farmer.on_connect,
        network_id=network_id,
        rpc_info=rpc_info,
        connect_to_daemon=connect_to_daemon,
    )


async def async_main() -> int:
    # TODO: refactor to avoid the double load
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    service_config = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", SERVICE_NAME)
    config[SERVICE_NAME] = service_config
    config_pool = load_config_cli(DEFAULT_ROOT_PATH, "config.yaml", "pool")
    config["pool"] = config_pool
    initialize_service_logging(service_name=SERVICE_NAME, config=config)
    service = create_farmer_service(DEFAULT_ROOT_PATH, config, config_pool, DEFAULT_CONSTANTS)
    await service.setup_process_global_state()
    await service.run()

    return 0


def main() -> int:
    return async_run(async_main())


if __name__ == "__main__":
    sys.exit(main())
