from __future__ import annotations

from typing import Generator, KeysView

SERVICES_FOR_GROUP = {
    "all": [
        "dogechia_harvester",
        "dogechia_timelord_launcher",
        "dogechia_timelord",
        "dogechia_farmer",
        "dogechia_full_node",
        "dogechia_wallet",
        "dogechia_data_layer",
        "dogechia_data_layer_http",
    ],
    # TODO: should this be `data_layer`?
    "data": ["dogechia_wallet", "dogechia_data_layer"],
    "data_layer_http": ["dogechia_data_layer_http"],
    "node": ["dogechia_full_node"],
    "harvester": ["dogechia_harvester"],
    "farmer": ["dogechia_harvester", "dogechia_farmer", "dogechia_full_node", "dogechia_wallet"],
    "farmer-no-wallet": ["dogechia_harvester", "dogechia_farmer", "dogechia_full_node"],
    "farmer-only": ["dogechia_farmer"],
    "timelord": ["dogechia_timelord_launcher", "dogechia_timelord", "dogechia_full_node"],
    "timelord-only": ["dogechia_timelord"],
    "timelord-launcher-only": ["dogechia_timelord_launcher"],
    "wallet": ["dogechia_wallet"],
    "introducer": ["dogechia_introducer"],
    "simulator": ["dogechia_full_node_simulator"],
    "crawler": ["dogechia_crawler"],
    "seeder": ["dogechia_crawler", "dogechia_seeder"],
    "seeder-only": ["dogechia_seeder"],
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
