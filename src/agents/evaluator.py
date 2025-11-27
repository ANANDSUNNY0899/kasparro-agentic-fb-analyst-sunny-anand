

"""
EvaluatorAgent
--------------
Validate each hypothesis quantitatively and produce final verdicts and evidence.
Simple logic: compute pct change, judge supported/inconclusive, build evidence payload.
"""
import math

class EvaluatorAgent:

    def __init__(self):
        pass

    def validate(self, plan, hyp_bundle, data_summary):
        results = []
        camp_stats = {c["campaign"]: c for c in data_summary.get("campaign_stats", [])}

        for h in hyp_bundle.get("hypotheses", []):
            camp = h.get("campaign")
            stats = camp_stats.get(camp)
            if not stats:
                results.append({
                    "id": h.get("id"),
                    "campaign": camp,
                    "hypothesis": h.get("hypothesis"),
                    "verdict": "inconclusive",
                    "confidence": 0.35,
                    "evidence": {}
                })
                continue

            prior_ctr = stats.get("prior_ctr") or 0.0
            recent_ctr = stats.get("recent_ctr") or 0.0
            pct_change = stats.get("pct_change_ctr")

            # basic decision rules
            if pct_change is None:
                verdict = "inconclusive"
                confidence = 0.4
            else:
                if pct_change < -25:
                    verdict = "supported"
                    confidence = 0.85
                elif pct_change < -10:
                    verdict = "supported"
                    confidence = 0.65
                elif pct_change < -5:
                    verdict = "inconclusive"
                    confidence = 0.5
                else:
                    verdict = "not_supported"
                    confidence = 0.35

            evidence = {
                "prior_ctr": prior_ctr,
                "recent_ctr": recent_ctr,
                "pct_change_ctr": pct_change,
                "recent_impressions": stats.get("recent_impressions")
            }

            results.append({
                "id": h.get("id"),
                "campaign": camp,
                "hypothesis": h.get("hypothesis"),
                "verdict": verdict,
                "confidence": round(confidence, 2),
                "evidence": evidence
            })

        return {"validations": results}

    def generate_report(self, query, data_summary, validated, creatives):
        lines = [
            f"# Final Report — {query}",
            "",
            f"Date Range: {data_summary['date_range']['start']} → {data_summary['date_range']['end']}",
            "",
            "## Validated Insights",
        ]

        for v in validated["validations"]:
            lines.append(f"- **{v['campaign']}** — *{v['verdict']}* (conf {v['confidence']})")
            ev = v.get("evidence", {})
            lines.append(f"  Evidence: prior_ctr={ev.get('prior_ctr')}, recent_ctr={ev.get('recent_ctr')}, pct_change={ev.get('pct_change_ctr')}, recent_imps={ev.get('recent_impressions')}\n")

        lines.append("\n## Creative Recommendations\n")
        for c in creatives.get("recommendations", []):
            lines.append(f"### {c['campaign']}\nBaseline CTR: {c.get('baseline_ctr')}\nKeywords: {', '.join(c.get('keywords',[])[:5])}\nVariants:\n")
            for v in c.get("variants", []):
                lines.append(f"- {v['headline']} | {v['cta']} | {v.get('rationale')}\n")
            lines.append(f"A/B plan: {c.get('ab_test_plan')}\n\n")
        return "\n".join(lines)
