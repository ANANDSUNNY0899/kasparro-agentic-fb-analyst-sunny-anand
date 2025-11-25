"""
InsightAgent
------------
Reads data summary and creates hypotheses explaining performance drops
using Think → Analyze → Conclude reasoning.
"""





import uuid

class InsightAgent:

    def generate(self, plan, data_summary):

        hyps = []

        for row in data_summary["low_ctr_campaigns"]:
            h_id = str(uuid.uuid4())[:8]

            reason = "creative_underperformance"
            if row["pct_change_ctr"] is not None and row["pct_change_ctr"] < -20:
                reason = "creative_drop_detected"

            hyps.append({
                "id": h_id,
                "campaign": row["campaign_name"],
                "hypothesis": f"CTR drop due to {reason}",
                "think": f"recent_ctr={row['recent_ctr']}, prior_ctr={row['prior_ctr']}",
                "analyze": "compare CTR before vs after creative changes",
                "confidence": 0.5,
            })

        if not hyps:
            hyps.append({
                "id": "H-GENERAL",
                "campaign": "ALL",
                "hypothesis": "No low-CTR campaigns detected; ROAS fluctuations may be spend or seasonality related.",
                "confidence": 0.4,
            })

        return {"hypotheses": hyps}
