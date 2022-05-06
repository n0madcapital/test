from brownie import accounts, config, FundMe, network, MockV3Aggregator
import time
from scripts.helpful_scripts import get_account
from web3 import Web3


def fund_er():
    fund_me = FundMe[-1]
    account = get_account()
    print(fund_me.getPrice())
    print(fund_me.getEntranceFee())
    fund_me.fund({"from": account, "value": Web3.toWei(0.01, "ether")})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})
    print(f"left balance is {fund_me.getBalance()}")


def main():
    fund_er()
