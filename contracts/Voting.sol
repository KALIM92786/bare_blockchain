// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Voting {
    mapping(address => bool) public hasVoted;
    mapping(uint256 => uint256) public votes;
    uint256 public totalVotes;

    event VoteCast(address indexed voter, uint256 candidateId, uint256 voteCount);

    function vote(uint256 candidateId) public {
        require(!hasVoted[msg.sender], "Already voted");
        hasVoted[msg.sender] = true;
        votes[candidateId]++;
        totalVotes++;
        emit VoteCast(msg.sender, candidateId, votes[candidateId]);
    }

    function getVotes(uint256 candidateId) public view returns (uint256) {
        return votes[candidateId];
    }
}
