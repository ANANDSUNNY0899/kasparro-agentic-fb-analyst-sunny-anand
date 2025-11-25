"""
DataAgent
---------
Loads dataset, computes CTR/ROAS and aggregates
recent vs prior performance.
Also identifies low-performing campaigns using percentile thresholds.
"""





import pandas as pd
import numpy as np
from datetime import timedelta

class DataAgent:

    def __init__(self, csv_path="data/synthetic_fb_ads_undergarments.csv"):
        self.csv_path = csv_path

    def summarize(self, plan):

        df = pd.read_csv(self.csv_path, parse_dates=["date"])

        # Fill CTR if missing
        df["ctr"] = df.apply(
            lambda r: r["clicks"] / r["impressions"] if r["impressions"] > 0 else 0,
            axis=1,
        )

        # Windows
        recent_days = plan["windows"]["recent_days"]
        prior_days = plan["windows"]["prior_days"]

        max_date = df["date"].max()
        recent_cutoff = max_date - timedelta(days=recent_days)
        prior_cutoff = recent_cutoff - timedelta(days=prior_days)

        recent = df[df["date"] > recent_cutoff]
        prior = df[(df["date"] > prior_cutoff) & (df["date"] <= recent_cutoff)]

        # Aggregate stats
        def agg(sub):
            g = sub.groupby("campaign_name").agg(
                spend=("spend", "sum"),
                impressions=("impressions", "sum"),
                clicks=("clicks", "sum"),
                ctr=("ctr", "mean"),
                purchases=("purchases", "sum"),
                revenue=("revenue", "sum"),
            ).reset_index()
            g["roas"] = g["revenue"] / g["spend"].replace(0, np.nan)
            return g

        recent_stats = agg(recent)
        prior_stats = agg(prior)

        merged = recent_stats.merge(
            prior_stats, on="campaign_name", how="left", suffixes=("", "_prior")
        ).fillna(0)

        rows = []
        for _, r in merged.iterrows():
            prior_ctr = r["ctr_prior"]
            recent_ctr = r["ctr"]

            pct_ctr = ((recent_ctr - prior_ctr) / prior_ctr) * 100 if prior_ctr > 0 else None

            rows.append({
                "campaign_name": r["campaign_name"],
                "recent_ctr": float(recent_ctr),
                "prior_ctr": float(prior_ctr),
                "pct_change_ctr": pct_ctr,
                "recent_impressions": int(r["impressions"]),
                "prior_impressions": int(r["impressions_prior"]),
                "recent_roas": float(r["roas"]) if not np.isnan(r["roas"]) else None,
            })

        summary = {
            "date_range": {"start": str(df["date"].min().date()), "end": str(max_date.date())},
            "campaign_stats": rows,
            "low_ctr_threshold": None
        }

        # Identify low-CTR campaigns (bottom X percentile)
        valid = [r for r in rows if r["recent_impressions"] >= plan["thresholds"]["min_impressions"]]
        ctrs = [r["recent_ctr"] for r in valid]

        if ctrs:
            threshold = float(np.percentile(ctrs, plan["thresholds"]["low_ctr_percentile"]))
            summary["low_ctr_threshold"] = threshold
            summary["low_ctr_campaigns"] = [r for r in rows if r["recent_ctr"] <= threshold]
        else:
            summary["low_ctr_campaigns"] = []

        return summary
