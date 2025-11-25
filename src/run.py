import argparse
import json
import os
import datetime

from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.evaluator import EvaluatorAgent
from agents.creative_agent import CreativeAgent


def ensure_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main(query: str):

    RUN_ID = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Create output dirs
    ensure_dirs("reports")
    ensure_dirs("logs")
    ensure_dirs(f"logs/{RUN_ID}")

    # Initialize agents
    planner = PlannerAgent()
    data_agent = DataAgent()
    insight_agent = InsightAgent()
    evaluator = EvaluatorAgent()
    creative_agent = CreativeAgent()

    # ----------- PHASE 1: PLANNING -----------
    plan = planner.create_plan(query)
    with open(f"logs/{RUN_ID}/planner.json", "w") as f:
        json.dump(plan, f, indent=2)

    # ----------- PHASE 2: DATA SUMMARY -----------
    data_summary = data_agent.summarize(plan)
    with open(f"logs/{RUN_ID}/data_summary.json", "w") as f:
        json.dump(data_summary, f, indent=2)

    # ----------- PHASE 3: INSIGHTS / HYPOTHESES -----------
    hypotheses = insight_agent.generate(plan, data_summary)
    with open(f"logs/{RUN_ID}/hypotheses.json", "w") as f:
        json.dump(hypotheses, f, indent=2)

    # ----------- PHASE 4: EVALUATION -----------
    validated = evaluator.validate(plan, hypotheses, data_summary)
    with open(f"reports/insights.json", "w") as f:
        json.dump(validated, f, indent=2)

    # ----------- PHASE 5: CREATIVE IMPROVEMENTS -----------
    creatives = creative_agent.generate(plan, data_summary, validated)
    with open(f"reports/creatives.json", "w") as f:
        json.dump(creatives, f, indent=2)

    # ----------- PHASE 6: FINAL REPORT -----------
    report_text = evaluator.generate_report(query, data_summary, validated, creatives)
    with open(f"reports/report.md", "w") as f:
        f.write(report_text)

    print("\n🎉 Run complete.")
    print("Generated:")
    print("- reports/insights.json")
    print("- reports/creatives.json")
    print("- reports/report.md")
    print(f"- logs stored in logs/{RUN_ID}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Example: 'Analyze ROAS drop'")
    args = parser.parse_args()
    main(args.query)
