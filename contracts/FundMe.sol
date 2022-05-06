// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; //same as openzepplin's, checks for overflows, after sol 0.8 it is not necessary to use SafeMath

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        //will be executed whenever the contract is deployed
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        //uint256 minimumUSD = 0;
        //require(getConversionRate(msg.value) >= minimumUSD, "stop being broke");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        return 0;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        return
            (_ethAmount * getPrice()) /
            10**(uint256(priceFeed.decimals()) + 10);
    }

    //modifier is used to change the behavior of a function in declarative way
    modifier onlyOwner() {
        require(msg.sender == owner); //before running a function do this first
        _; //_ = rest of the code
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function withdraw() public onlyOwner {
        //run onlyOwner than contract
        msg.sender.transfer(address(this).balance); //address(this).balance gives the eth in contract
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0); //resets funders array
    }
}
