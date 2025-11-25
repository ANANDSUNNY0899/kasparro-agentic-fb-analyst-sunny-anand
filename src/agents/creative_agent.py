"""
CreativeAgent
-------------
Generates new creative concepts for low CTR campaigns.
Provides 5 diverse headline concepts per campaign,
each with CTA and expected CTR lift.
Includes A/B testing plan.
"""









import random

class CreativeAgent:

    def generate(self, plan, data_summary, validated):

        recs = []

        for row in data_summary["low_ctr_campaigns"]:

            campaign = row["campaign_name"]
            base_ctr = row["recent_ctr"]

            variants = []
            for i in range(5):
                headline = f"{campaign} — Save {10 + i*5}% Today"
                desc = "Limited stock • Free delivery • Easy returns"
                cta = random.choice(["Shop Now", "Learn More", "Grab Offer"])

                variants.append({
                    "headline": headline,
                    "description": desc,
                    "cta": cta,
                    "expected_lift": "+10% CTR"
                })

            recs.append({
                "campaign": campaign,
                "baseline_ctr": base_ctr,
                "variants": variants,
                "ab_plan": {"metric": "CTR", "min_sample": 2000}
            })

        return {"recommendations": recs}
