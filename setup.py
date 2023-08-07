from __future__ import annotations

import os
import sys

from setuptools import setup

dependencies = [
    "aiofiles==23.1.0",  # Async IO for files
    "anyio==3.6.2",
    "boto3==1.26.131",  # AWS S3 for DL s3 plugin
    "blspy==1.0.16",  # Signature library
    "chiavdf==1.0.9",  # timelord and vdf verification
    "chiabip158==1.2",  # bip158-style wallet filters
    "chiapos==1.0.11",  # proof of space
    "clvm==0.9.7",
    "clvm_tools==0.4.6",  # Currying, Program.to, other conveniences
    "chia_rs==0.2.7",
    "clvm-tools-rs==0.1.30",  # Rust implementation of clvm_tools' compiler
    "aiohttp==3.8.4",  # HTTP server for full node rpc
    "aiosqlite==0.19.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==4.0.2",  # Binary data management library
    "colorama==0.4.6",  # Colorizes terminal output
    "colorlog==6.7.0",  # Adds color to logs
    "concurrent-log-handler==0.9.24",  # Concurrently log and rotate logs
    "cryptography==40.0.2",  # Python cryptography library for TLS - keyring conflict
    "filelock==3.12.0",  # For reading and writing config multiprocess and multithread safely  (non-reentrant locks)
    "keyring==23.13.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "PyYAML==6.0",  # Used for config file format
    "setproctitle==1.3.2",  # Gives the dogechia processes readable names
    "sortedcontainers==2.4.0",  # For maintaining sorted mempools
    "click==8.1.3",  # For the CLI
    "dnspython==2.3.0",  # Query DNS seeds
    "watchdog==2.2.0",  # Filesystem event watching - watches keyring.yaml
    "dnslib==0.9.23",  # dns lib
    "typing-extensions==4.6.0",  # typing backports like Protocol and TypedDict
    "zstd==1.5.5.1",
    "packaging==23.1",
    "psutil==5.9.4",
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "build",
    # >=7.2.4 for https://github.com/nedbat/coveragepy/issues/1604
    "coverage>=7.2.4",
    "diff-cover",
    "pre-commit",
    "py3createtorrent",
    "pylint",
    "pytest",
    "pytest-asyncio>=0.18.1",  # require attribute 'fixture'
    "pytest-cov",
    "pytest-monitor; sys_platform == 'linux'",
    "pytest-xdist",
    "twine",
    "isort",
    "flake8",
    "mypy==1.3.0",
    "black==23.3.0",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
    "pyinstaller==5.11.0",
    "types-aiofiles",
    "types-cryptography",
    "types-pkg_resources",
    "types-pyyaml",
    "types-setuptools",
]

legacy_keyring_dependencies = [
    "keyrings.cryptfile==1.3.9",
]

kwargs = dict(
    name="doge-chia",
    author="Mariano Sorgente",
    author_email="mariano@dogechi.org",
    description="Dogechia blockchain full node, farmer, timelord, and wallet.",
    url="https://dogechi.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="dogechia blockchain node",
    install_requires=dependencies,
    extras_require=dict(
        dev=dev_dependencies,
        upnp=upnp_dependencies,
        legacy_keyring=legacy_keyring_dependencies,
    ),
    packages=[
        "build_scripts",
        "dogechia",
        "dogechia.cmds",
        "dogechia.clvm",
        "dogechia.consensus",
        "dogechia.daemon",
        "dogechia.data_layer",
        "dogechia.full_node",
        "dogechia.timelord",
        "dogechia.farmer",
        "dogechia.harvester",
        "dogechia.introducer",
        "dogechia.plot_sync",
        "dogechia.plotters",
        "dogechia.plotting",
        "dogechia.pools",
        "dogechia.protocols",
        "dogechia.rpc",
        "dogechia.seeder",
        "dogechia.server",
        "dogechia.simulator",
        "dogechia.types.blockchain_format",
        "dogechia.types",
        "dogechia.util",
        "dogechia.wallet",
        "dogechia.wallet.db_wallet",
        "dogechia.wallet.puzzles",
        "dogechia.wallet.cat_wallet",
        "dogechia.wallet.did_wallet",
        "dogechia.wallet.nft_wallet",
        "dogechia.wallet.trading",
        "dogechia.wallet.util",
        "dogechia.wallet.vc_wallet",
        "dogechia.wallet.vc_wallet.vc_puzzles",
        "dogechia.wallet.vc_wallet.cr_puzzles",
        "dogechia.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "dogechia = dogechia.cmds.dogechia:main",
            "dogechia_daemon = dogechia.daemon.server:main",
            "dogechia_wallet = dogechia.server.start_wallet:main",
            "dogechia_full_node = dogechia.server.start_full_node:main",
            "dogechia_harvester = dogechia.server.start_harvester:main",
            "dogechia_farmer = dogechia.server.start_farmer:main",
            "dogechia_introducer = dogechia.server.start_introducer:main",
            "dogechia_crawler = dogechia.seeder.start_crawler:main",
            "dogechia_seeder = dogechia.seeder.dns_server:main",
            "dogechia_timelord = dogechia.server.start_timelord:main",
            "dogechia_timelord_launcher = dogechia.timelord.timelord_launcher:main",
            "dogechia_full_node_simulator = dogechia.simulator.start_simulator:main",
            "dogechia_data_layer = dogechia.server.start_data_layer:main",
            "dogechia_data_layer_http = dogechia.data_layer.data_layer_server:main",
            "dogechia_data_layer_s3_plugin = dogechia.data_layer.s3_plugin_service:run_server",
        ]
    },
    package_data={
        "dogechia": ["pyinstaller.spec"],
        "": ["*.clsp", "*.clsp.hex", "*.clvm", "*.clib", "py.typed"],
        "dogechia.util": ["initial-*.yaml", "english.txt"],
        "dogechia.ssl": ["dogechia_ca.crt", "dogechia_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    project_urls={
        "Source": "https://github.com/blockchiansea/doge-chia/",
        "Changelog": "https://github.com/blockchiansea/doge-chia/blob/main/CHANGELOG.md",
    },
)

if "setup_file" in sys.modules:
    # include dev deps in regular deps when run in snyk
    dependencies.extend(dev_dependencies)

if len(os.environ.get("DOGECHIA_SKIP_SETUP", "")) < 1:
    setup(**kwargs)  # type: ignore
