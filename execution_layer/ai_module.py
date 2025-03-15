class AI_Module:
    def analyze_transaction(self, transaction):
        """
        Analyze a transaction and return a risk score and recommendation.
        For this demo, a simple rule-based approach is used.
        """
        amount = transaction.get("amount", 0)
        if amount > 1000:
            risk_score = 0.9
            recommendation = "High risk: Review transaction manually."
        else:
            risk_score = 0.1
            recommendation = "Low risk: Transaction is acceptable."
        print(f"Analyzing transaction: amount={amount}, risk_score={risk_score}")
        return {"risk_score": risk_score, "recommendation": recommendation}
