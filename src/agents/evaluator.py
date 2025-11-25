"""
EvaluatorAgent
--------------
Validates hypotheses using quantitative checks:
- Before/after CTR comparison
- % drop evaluation
- Confidence scoring
Produces supported / not-supported / inconclusive verdicts.
"""








import numpy as np

class EvaluatorAgent:

    def validate(self, plan, hyp_bundle, data_summary):

        validations = []

        for h in hyp_bundle["hypotheses"]:
            # fallback: find campaign stats
            stats = next(
                (c for c in data_summary["campaign_stats"] if c["campaign_name"] == h["campaign"]),
                None,
            )

            if not stats:
                validations.append({
                    "id": h["id"],
                    "campaign": h["campaign"],
                    "verdict": "inconclusive",
                    "confidence": 0.3
                })
                continue

            before = stats["prior_ctr"]
            after = stats["recent_ctr"]

            if before > 0:
                diff = ((after - before) / before) * 100
            else:
                diff = None

            verdict = "supported" if diff is not None and diff < -20 else "not_supported"
            confidence = 0.8 if verdict == "supported" else 0.4

            validations.append({
                "id": h["id"],
                "campaign": h["campaign"],
                "hypothesis": h["hypothesis"],
                "verdict": verdict,
                "confidence": confidence,
                "evidence": {
                    "before_ctr": before,
                    "after_ctr": after,
                    "pct_change": diff
                }
            })

        return {"validations": validations}

    def generate_report(self, query, data_summary, validated, creatives):

        lines = [
            f"# Final Report — {query}",
            "",
            f"Date Range: {data_summary['date_range']['start']} → {data_summary['date_range']['end']}",
            "",
            "## Validated Insights",
        ]

        for v in validated["validations"]:
            lines.append(
                f"- **{v['campaign']}** — *{v['verdict']}* (conf {v['confidence']})"
            )

        lines.append("\n## Creative Recommendations\n")

        for c in creatives["recommendations"]:
            lines.append(f"### {c['campaign']}")
            for v in c["variants"]:
                lines.append(f"- {v['headline']} — {v['cta']}")

        return "\n".join(lines)
