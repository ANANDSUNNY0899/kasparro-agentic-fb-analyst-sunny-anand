"""
PlannerAgent
------------
Interprets user query and produces a structured plan defining:
- Time windows
- Thresholds
- Sequence of agent steps
This acts as the 'brain' of the pipeline.
"""






import datetime

class PlannerAgent:

    def __init__(self):
        pass

    def create_plan(self, query: str):

        plan = {
            "query": query,
            "created_at": datetime.datetime.utcnow().isoformat(),

            "windows": {
                "recent_days": 30,
                "prior_days": 30,
                "short_days": 7
            },

            "thresholds": {
                "low_ctr_percentile": 15,
                "min_impressions": 500,
                "confidence_min": 0.60
            },

            "steps": [
                "data_summary",
                "insight_generation",
                "evaluation",
                "creative_generation"
            ]
        }

        return plan
