from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fundme
from scripts.getprice import fund_er
from brownie import network, accounts, config, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fundme()
    fee = fund_me.getEntranceFee()
    fund_me.fund({"from": account, "value": Web3.toWei(0.01, "ether")}).wait(1)
    assert fund_me.addressToAmountFunded(account) == Web3.toWei(0.01, "ether")
    fund_me.withdraw({"from": account}).wait(1)
    assert fund_me.getBalance() == 0


def test_only_owner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("deez nuts")
    account = get_account()
    fund_me = deploy_fundme()
    fee = fund_me.getEntranceFee()
    fund_me.fund({"from": account, "value": Web3.toWei(0.01, "ether")}).wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw(
            {
                "from": accounts.add(config["wallets"]["from_key_two"]),
                "gas_price": 0,
                "gas_limit": 12000000,
                "allow_revert": True,
            }
        )
