# """
# InsightAgent
# ------------
# Reads data summary and creates hypotheses explaining performance drops
# using Think → Analyze → Conclude reasoning.
# """





# import uuid

# class InsightAgent:

#     def generate(self, plan, data_summary):

#         hyps = []

#         for row in data_summary["low_ctr_campaigns"]:
#             h_id = str(uuid.uuid4())[:8]

#             reason = "creative_underperformance"
#             if row["pct_change_ctr"] is not None and row["pct_change_ctr"] < -20:
#                 reason = "creative_drop_detected"

#             hyps.append({
#                 "id": h_id,
#                 "campaign": row["campaign_name"],
#                 "hypothesis": f"CTR drop due to {reason}",
#                 "think": f"recent_ctr={row['recent_ctr']}, prior_ctr={row['prior_ctr']}",
#                 "analyze": "compare CTR before vs after creative changes",
#                 "confidence": 0.5,
#             })

#         if not hyps:
#             hyps.append({
#                 "id": "H-GENERAL",
#                 "campaign": "ALL",
#                 "hypothesis": "No low-CTR campaigns detected; ROAS fluctuations may be spend or seasonality related.",
#                 "confidence": 0.4,
#             })

#         return {"hypotheses": hyps}








"""
InsightAgent
------------
Create hypotheses grounded in actual per-campaign metrics and creative messages.
Rules:
 - If % CTR drop < -20% -> creative_drop_detected
 - If platform/geo shows lower CTR than baseline -> audience/platform signal
 - If impressions >> prior and CTR down -> possible audience fatigue
"""
import uuid
import math

class InsightAgent:

    def __init__(self):
        pass

    def generate(self, plan, data_summary):
        hyps = []
        campaigns = data_summary.get("low_ctr_campaigns", [])
        creative_details = data_summary.get("creative_details", {})

        for c in campaigns:
            camp = c["campaign"]
            prior = c.get("prior_ctr") or 0.0
            recent = c.get("recent_ctr") or 0.0
            pct = c.get("pct_change_ctr")
            reasons = []
            # rule: major CTR drop
            if pct is not None and pct < -20:
                reasons.append("creative_drop_detected")
            # rule: impressions grew a lot while CTR fell
            if c["prior_impressions"]>0 and c["recent_impressions"] > c["prior_impressions"] * 1.25 and (pct is None or pct < 0):
                reasons.append("audience_fatigue_or_overexposure")
            # rule: check top creative variety (if single creative dominates)
            top_msgs = creative_details.get(camp, [])
            if top_msgs:
                top_share = top_msgs[0]["impressions"] / (sum([x["impressions"] for x in top_msgs]) + 1e-9)
                if top_share > 0.6:
                    reasons.append("creative_over_reliance")
            if not reasons:
                reasons.append("creative_underperformance")

            evidence = {
                "prior_ctr": prior,
                "recent_ctr": recent,
                "pct_change_ctr": pct,
                "top_creatives_sample": top_msgs[:3]
            }

            hyps.append({
                "id": f"H-{uuid.uuid4().hex[:8]}",
                "campaign": camp,
                "hypothesis": " or ".join(reasons),
                "think": f"recent_ctr={recent:.4f}, prior_ctr={prior:.4f}, pct_change={pct}",
                "analyze": "rules-based checks over campaign + creative stats",
                "evidence": evidence,
                "confidence": 0.6 + min(0.3, max(0.0, (-pct or 0)/100)) if pct is not None else 0.5
            })
        if not hyps:
            hyps.append({
                "id": "H-GLOBAL-000",
                "campaign": "ALL",
                "hypothesis": "No low-CTR campaigns detected in this window. Inspect spend shifts/seasonality.",
                "think": "",
                "analyze": "",
                "evidence": {},
                "confidence": 0.4
            })
        return {"hypotheses": hyps}
