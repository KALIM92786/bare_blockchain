# governance/governance.py
import time
import logging

class GovernanceProposal:
    def __init__(self, proposal_id, proposer, description, proposal_type, voting_period):
        """
        Initialize a new governance proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param proposer: Address of the proposer.
        :param description: Brief description of the proposal.
        :param proposal_type: Type/category of the proposal (e.g., parameter change, contract upgrade).
        :param voting_period: Duration (in seconds) for which voting is open.
        """
        self.proposal_id = proposal_id
        self.proposer = proposer
        self.description = description
        self.proposal_type = proposal_type
        self.voting_deadline = time.time() + voting_period  # Voting deadline timestamp
        self.votes = {}  # Mapping: voter address -> vote (True for yes, False for no)
        self.executed = False

    def cast_vote(self, voter, vote):
        """
        Cast a vote on the proposal.
        :param voter: Address of the voter.
        :param vote: Boolean vote (True for yes, False for no).
        :raises Exception: if the voting period has ended or voter already voted.
        """
        if time.time() > self.voting_deadline:
            raise Exception("Voting period has ended")
        if voter in self.votes:
            raise Exception("Voter has already cast a vote")
        self.votes[voter] = vote
        logging.info(f"Voter {voter} voted {'YES' if vote else 'NO'} on proposal {self.proposal_id}")

    def tally_votes(self):
        """
        Tally the votes on the proposal.
        :return: A dictionary with counts of yes and no votes.
        """
        yes_votes = sum(1 for vote in self.votes.values() if vote)
        no_votes = sum(1 for vote in self.votes.values() if not vote)
        return {"yes": yes_votes, "no": no_votes}

    def is_passed(self, threshold=0.5):
        """
        Determine whether the proposal has passed.
        :param threshold: The fraction of yes votes required for the proposal to pass.
        :return: True if the proposal passes, else False.
        """
        tally = self.tally_votes()
        total_votes = tally["yes"] + tally["no"]
        if total_votes == 0:
            return False
        return (tally["yes"] / total_votes) > threshold

    def __repr__(self):
        return (f"GovernanceProposal(proposal_id={self.proposal_id}, proposer={self.proposer}, "
                f"description={self.description}, proposal_type={self.proposal_type}, "
                f"voting_deadline={self.voting_deadline}, votes={self.votes}, executed={self.executed})")
