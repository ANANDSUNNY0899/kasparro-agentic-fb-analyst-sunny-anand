

"""
CreativeAgent
-------------
Use real `creative_message` texts to extract keywords and produce grounded creative variants.
Variants vary by tone: Emotional, Urgency, Value, Problem→Solution, Social Proof.
"""
import re
from collections import Counter
from math import ceil

class CreativeAgent:

    def __init__(self):
        pass

    @staticmethod
    def extract_keywords(messages, top_k=6):
        toks = []
        stop = set(["the","and","with","for","your","a","to","in","of","on","is","our","we","get","now","you","that","it","this"])
        for m in messages:
            if not isinstance(m, str):
                continue
            words = re.findall(r"[A-Za-z']+", m.lower())
            toks.extend([w for w in words if w not in stop and len(w)>2])
        common = [w for w,_ in Counter(toks).most_common(top_k)]
        return common

    def generate(self, plan, data_summary, validated):
        recs = []
        creative_details = data_summary.get("creative_details", {})

        for v in validated.get("validations", []):
            camp = v["campaign"]
            # skip of vague campaigns
            if camp == "ALL":
                continue
            top_msgs = creative_details.get(camp, [])
            messages = [m["creative_message"] for m in top_msgs if isinstance(m.get("creative_message",""), str)]
            if not messages:
                # fallback generic variants but still based on camp name
                keywords = camp.split()[:3]
            else:
                keywords = self.extract_keywords(messages, top_k=6)

            # produce 5 variants with different tones
            variants = []
            tones = [
                ("Emotional","Feel-comfort", "+10%"),
                ("Urgency","Limited-stock", "+15%"),
                ("Value","Affordable-quality", "+9%"),
                ("Problem→Solution","Comfort-solution", "+18%"),
                ("SocialProof","Top-rated", "+12%")
            ]
            for i, (tone, tag, lift) in enumerate(tones):
                kw = (keywords[i] if i < len(keywords) else (camp.split()[0] if camp else "Shop"))
                headline = f"{kw.title()} — { 'All-day comfort' if tone=='Emotional' else ('Limited time — restock' if tone=='Urgency' else ('Premium comfort at great price' if tone=='Value' else ('Fix your fit today' if tone=='Problem→Solution' else 'Loved by thousands')))}"
                desc = " ".join(keywords[:4]).title() + " • Free returns" if keywords else "Comfortable • Easy returns"
                cta = ["Experience Comfort","Shop Now","Upgrade Today","Fix My Fit","See Why"][i%5]
                variants.append({
                    "headline": headline,
                    "description": desc,
                    "cta": cta,
                    "rationale": f"Tone={tone}; anchored to keywords {keywords[:3]}",
                    "expected_impact": lift
                })

            # a/b plan
            recent_imps = 0
            stats = next((c for c in data_summary.get("campaign_stats", []) if c["campaign"]==camp), {})
            recent_imps = stats.get("recent_impressions", 0)
            ab_plan = {"metric":"CTR", "min_sample_per_variant": max(1000, ceil(recent_imps*0.05)), "duration_days":7}

            recs.append({
                "campaign": camp,
                "baseline_ctr": stats.get("recent_ctr"),
                "keywords": keywords,
                "variants": variants,
                "ab_test_plan": ab_plan
            })

        return {"recommendations": recs}
