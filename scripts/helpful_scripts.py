from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 18
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
STARTING_PRICE = 2
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["developement", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"active network {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS,
            Web3.toWei(STARTING_PRICE, "ether"),
            {"from": get_account()},  # toWei adds 18 decimals
        )
