from brownie import (
    accounts,
    config,
    FundMe,
    network,
    MockV3Aggregator,
)
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    deploy_mocks,
)
from web3 import Web3
from scripts.getprice import fund_er, withdraw


def deploy_fundme():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fundme = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # publish_source=True to verify the contract
    print(f"Contract deployed to {fundme.address}")
    for x in range(5):
        print(5 - x)
    return fundme


def main():
    deploy_fundme()
    fund_er()
