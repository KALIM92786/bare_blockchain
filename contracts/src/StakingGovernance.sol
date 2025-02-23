// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

// Minimal ERC20 interface to interact with BareCoin
interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract StakingGovernance {
    struct Staker {
        uint256 amount;     // Tokens staked
        uint256 reward;     // Accumulated reward tokens
        uint256 lastStaked; // Timestamp of the last stake or reward claim
    }

    IERC20 public token; // BareCoin token
    address public owner;
    uint256 public totalStaked;
    uint256 public rewardRate;    // Annual reward rate (e.g., 5 means 5% per year)
    uint256 public minStakeAmount; // Minimum stake required

    mapping(address => Staker) public stakers;

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 reward);
    event RewardWithdrawn(address indexed user, uint256 reward);
    event RewardRateAdjusted(uint256 newRate);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    /// @notice Constructor initializes the contract with the staking token address.
    /// @param _tokenAddress The address of the BareCoin token.
    constructor(address _tokenAddress) {
        owner = msg.sender;
        token = IERC20(_tokenAddress);
        rewardRate = 5; // Default reward rate: 5% per year
        minStakeAmount = 100 * 1e18; // Minimum stake: 100 tokens (assuming 18 decimals)
    }

    /// @notice Stake tokens to earn rewards.
    /// @param _amount The number of tokens to stake.
    function stake(uint256 _amount) public {
        require(_amount >= minStakeAmount, "Amount too low");
        // Transfer tokens from user to this contract (ensure user approved this transfer)
        require(token.transferFrom(msg.sender, address(this), _amount), "Token transfer failed");

        // If user is already staking, claim pending rewards first.
        if (stakers[msg.sender].amount > 0) {
            claimReward();
        } else {
            stakers[msg.sender].lastStaked = block.timestamp;
        }
        stakers[msg.sender].amount += _amount;
        totalStaked += _amount;
        emit Staked(msg.sender, _amount);
    }

    /// @notice Unstake tokens and transfer them back to the user.
    /// @param _amount The number of tokens to unstake.
    function unstake(uint256 _amount) public {
        require(stakers[msg.sender].amount >= _amount, "Insufficient staked amount");
        // Claim rewards before unstaking.
        claimReward();
        stakers[msg.sender].amount -= _amount;
        totalStaked -= _amount;
        require(token.transfer(msg.sender, _amount), "Token transfer failed");
        emit Unstaked(msg.sender, _amount);
    }

    /// @notice Claim and update rewards for the caller.
    function claimReward() public {
        Staker storage staker = stakers[msg.sender];
        require(staker.amount > 0, "No staked tokens");
        // Calculate reward based on staked amount, reward rate, and time elapsed.
        uint256 timeElapsed = block.timestamp - staker.lastStaked;
        uint256 rewardEarned = (staker.amount * rewardRate * timeElapsed) / (100 * 365 days);
        staker.reward += rewardEarned;
        staker.lastStaked = block.timestamp;
        emit RewardClaimed(msg.sender, rewardEarned);
    }

    /// @notice Withdraw accumulated reward tokens.
    function withdrawReward() public {
        Staker storage staker = stakers[msg.sender];
        require(staker.reward > 0, "No reward available");
        uint256 rewardAmount = staker.reward;
        staker.reward = 0;
        require(token.transfer(msg.sender, rewardAmount), "Reward transfer failed");
        emit RewardWithdrawn(msg.sender, rewardAmount);
    }

    /// @notice Adjust the annual reward rate. Only the contract owner can call this.
    /// @param _newRate The new annual reward rate (in percentage).
    function adjustRewardRate(uint256 _newRate) public onlyOwner {
        rewardRate = _newRate;
        emit RewardRateAdjusted(_newRate);
    }
}
