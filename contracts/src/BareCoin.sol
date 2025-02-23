// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BareCoin is ERC20 {
    constructor() ERC20("BareCoin", "BRC") {
        // Mint 1 trillion tokens to the deployer (assuming 18 decimals)
        uint256 initialSupply = 1_000_000_000_000 * 10 ** decimals();
        _mint(msg.sender, initialSupply);
    }
}
