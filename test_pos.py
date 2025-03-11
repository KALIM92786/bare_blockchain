from consensus.pos import ProofOfStake

def test_validator_selection():
    pos = ProofOfStake()
    pos.add_stake("validator1", 100)
    pos.add_stake("validator2", 50)
    selections = {}
    for _ in range(1000):
        validator = pos.select_validator()
        selections[validator] = selections.get(validator, 0) + 1
    print("Validator selections over 1000 iterations:", selections)

if __name__ == "__main__":
    test_validator_selection()
