# execution_layer/ai_module.py

class AI_Module:
    def analyze_transaction(self, transaction):
        """
        Analyze a transaction and return a risk score and recommendation.
        For this demo, we use a simple rule-based approach.
        You can later replace this with an ML model.
        """
        # For example, if the amount exceeds a threshold, mark as high risk.
        amount = transaction.get("amount", 0)
        if amount > 1000:
            risk_score = 0.9
            recommendation = "High risk: Review transaction manually."
        else:
            risk_score = 0.1
            recommendation = "Low risk: Transaction is acceptable."
        
        # Log the analysis (in a real scenario, more complex features would be used)
        print(f"Analyzing transaction: amount={amount}, risk_score={risk_score}")
        return {"risk_score": risk_score, "recommendation": recommendation}
