# """
# DataAgent
# ---------
# Loads dataset, computes CTR/ROAS and aggregates
# recent vs prior performance.
# Also identifies low-performing campaigns using percentile thresholds.
# """





# import pandas as pd
# import numpy as np
# from datetime import timedelta

# class DataAgent:

#     def __init__(self, csv_path="data/synthetic_fb_ads_undergarments.csv"):
#         self.csv_path = csv_path

#     def summarize(self, plan):

#         df = pd.read_csv(self.csv_path, parse_dates=["date"])

#         # Fill CTR if missing
#         df["ctr"] = df.apply(
#             lambda r: r["clicks"] / r["impressions"] if r["impressions"] > 0 else 0,
#             axis=1,
#         )

#         # Windows
#         recent_days = plan["windows"]["recent_days"]
#         prior_days = plan["windows"]["prior_days"]

#         max_date = df["date"].max()
#         recent_cutoff = max_date - timedelta(days=recent_days)
#         prior_cutoff = recent_cutoff - timedelta(days=prior_days)

#         recent = df[df["date"] > recent_cutoff]
#         prior = df[(df["date"] > prior_cutoff) & (df["date"] <= recent_cutoff)]

#         # Aggregate stats
#         def agg(sub):
#             g = sub.groupby("campaign_name").agg(
#                 spend=("spend", "sum"),
#                 impressions=("impressions", "sum"),
#                 clicks=("clicks", "sum"),
#                 ctr=("ctr", "mean"),
#                 purchases=("purchases", "sum"),
#                 revenue=("revenue", "sum"),
#             ).reset_index()
#             g["roas"] = g["revenue"] / g["spend"].replace(0, np.nan)
#             return g

#         recent_stats = agg(recent)
#         prior_stats = agg(prior)

#         merged = recent_stats.merge(
#             prior_stats, on="campaign_name", how="left", suffixes=("", "_prior")
#         ).fillna(0)

#         rows = []
#         for _, r in merged.iterrows():
#             prior_ctr = r["ctr_prior"]
#             recent_ctr = r["ctr"]

#             pct_ctr = ((recent_ctr - prior_ctr) / prior_ctr) * 100 if prior_ctr > 0 else None

#             rows.append({
#                 "campaign_name": r["campaign_name"],
#                 "recent_ctr": float(recent_ctr),
#                 "prior_ctr": float(prior_ctr),
#                 "pct_change_ctr": pct_ctr,
#                 "recent_impressions": int(r["impressions"]),
#                 "prior_impressions": int(r["impressions_prior"]),
#                 "recent_roas": float(r["roas"]) if not np.isnan(r["roas"]) else None,
#             })

#         summary = {
#             "date_range": {"start": str(df["date"].min().date()), "end": str(max_date.date())},
#             "campaign_stats": rows,
#             "low_ctr_threshold": None
#         }

#         # Identify low-CTR campaigns (bottom X percentile)
#         valid = [r for r in rows if r["recent_impressions"] >= plan["thresholds"]["min_impressions"]]
#         ctrs = [r["recent_ctr"] for r in valid]

#         if ctrs:
#             threshold = float(np.percentile(ctrs, plan["thresholds"]["low_ctr_percentile"]))
#             summary["low_ctr_threshold"] = threshold
#             summary["low_ctr_campaigns"] = [r for r in rows if r["recent_ctr"] <= threshold]
#         else:
#             summary["low_ctr_campaigns"] = []

#         return summary




"""
DataAgent
---------
Loads dataset, normalizes campaign names, computes per-campaign and per-creative
metrics (impressions, clicks, ctr, revenue, roas). Returns a structured summary
that downstream agents will use.
"""
import pandas as pd
import numpy as np
import re
from datetime import timedelta

class DataAgent:

    def __init__(self, csv_path="data/synthetic_fb_ads_undergarments.csv"):
        self.csv_path = csv_path

    @staticmethod
    def normalize_campaign(name):
        if not isinstance(name, str):
            return str(name)
        # collapse spaces, remove weird chars, lower, compact repeated spaces
        n = name.strip()
        n = re.sub(r'[_\-\|]+', ' ', n)            # replace underscores/pipes/dashes with space
        n = re.sub(r'\s+', ' ', n)                 # collapse multiple spaces
        n = n.strip()
        return n.title()

    def summarize(self, plan):
        # Read CSV
        df = pd.read_csv(self.csv_path, parse_dates=["date"], dayfirst=False)

        # Ensure numeric columns exist
        for c in ["spend","impressions","clicks","purchases","revenue","ctr","roas"]:
            if c not in df.columns:
                df[c] = 0

        # Recompute CTR defensively
        df["ctr"] = df.apply(lambda r: (r["clicks"] / r["impressions"]) if r["impressions"]>0 else 0.0, axis=1)
        df["campaign_norm"] = df["campaign_name"].apply(self.normalize_campaign)

        # Windows
        recent_days = plan["windows"]["recent_days"]
        prior_days = plan["windows"]["prior_days"]

        max_date = df["date"].max()
        recent_cutoff = max_date - timedelta(days=recent_days)
        prior_cutoff = recent_cutoff - timedelta(days=prior_days)

        recent = df[df["date"] > recent_cutoff]
        prior = df[(df["date"] > prior_cutoff) & (df["date"] <= recent_cutoff)]

        # Per campaign aggregates
        def agg(sub):
            g = sub.groupby("campaign_norm").agg(
                spend=("spend","sum"),
                impressions=("impressions","sum"),
                clicks=("clicks","sum"),
                ctr_mean=("ctr","mean"),
                purchases=("purchases","sum"),
                revenue=("revenue","sum")
            ).reset_index()
            g["roas"] = g.apply(lambda r: (r["revenue"]/r["spend"]) if r["spend"]>0 else None, axis=1)
            return g

        recent_stats = agg(recent)
        prior_stats = agg(prior)

        merged = recent_stats.merge(prior_stats, on="campaign_norm", how="left", suffixes=("","_prior")).fillna(0)

        campaign_stats = []
        for _, r in merged.iterrows():
            prior_ctr = float(r.get("ctr_mean_prior",0) or 0.0)
            recent_ctr = float(r.get("ctr_mean",0) or 0.0)
            pct_change_ctr = ((recent_ctr - prior_ctr)/prior_ctr*100) if prior_ctr>0 else None
            campaign_stats.append({
                "campaign": r["campaign_norm"],
                "recent_impressions": int(r["impressions"]),
                "recent_clicks": int(r["clicks"]),
                "recent_ctr": recent_ctr,
                "prior_impressions": int(r.get("impressions_prior",0)),
                "prior_clicks": int(r.get("clicks_prior",0)),
                "prior_ctr": prior_ctr,
                "pct_change_ctr": pct_change_ctr,
                "recent_revenue": float(r.get("revenue",0)),
                "recent_roas": float(r.get("roas")) if r.get("roas") not in (None, np.nan) else None
            })

        # Identify low-CTR campaigns (percentile among campaigns with some volume)
        valid = [c for c in campaign_stats if c["recent_impressions"] >= plan["thresholds"]["min_impressions"]]
        ctrs = [c["recent_ctr"] for c in valid]
        low_threshold = float(np.percentile(ctrs, plan["thresholds"]["low_ctr_percentile"])) if len(ctrs)>0 else None
        low_campaigns = [c for c in campaign_stats if low_threshold is not None and c["recent_ctr"] <= low_threshold]

        # For each low campaign, collect top creative messages and creative-level stats
        creative_details = {}
        for c in low_campaigns:
            camp_raw = c["campaign"]
            sub = df[df["campaign_norm"]==camp_raw]
            # creative-level aggregation
            creative_agg = sub.groupby("creative_message").agg(
                impressions=("impressions","sum"),
                clicks=("clicks","sum"),
                ctr_mean=("ctr","mean"),
                spend=("spend","sum"),
                revenue=("revenue","sum")
            ).reset_index().sort_values("impressions", ascending=False)
            top_messages = creative_agg.head(10).to_dict(orient="records")
            creative_details[camp_raw] = top_messages

        summary = {
            "date_range": {"start": str(df["date"].min().date()), "end": str(df["date"].max().date())},
            "campaign_stats": campaign_stats,
            "low_ctr_threshold": low_threshold,
            "low_ctr_campaigns": low_campaigns,
            "creative_details": creative_details,
            "raw_sample_rows": df.head(5).to_dict(orient="records")
        }
        return summary
