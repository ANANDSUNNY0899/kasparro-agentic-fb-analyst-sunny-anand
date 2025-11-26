# import argparse
# import json
# import os
# import datetime
# import pandas as pd
# from agents.planner import PlannerAgent
# from agents.data_agent import DataAgent
# from agents.insight_agent import InsightAgent
# from agents.evaluator import EvaluatorAgent
# from agents.creative_agent import CreativeAgent


# def ensure_dirs(path):
#     if not os.path.exists(path):
#         os.makedirs(path)


# # def main(query: str):

# #     RUN_ID = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

# #     # Create output dirs
# #     ensure_dirs("reports")
# #     ensure_dirs("logs")
# #     ensure_dirs(f"logs/{RUN_ID}")

# #     # Initialize agents
# #     planner = PlannerAgent()
# #     data_agent = DataAgent()
# #     insight_agent = InsightAgent()
# #     evaluator = EvaluatorAgent()
# #     creative_agent = CreativeAgent()

# #     # ----------- PHASE 1: PLANNING -----------
# #     plan = planner.create_plan(query)
# #     with open(f"logs/{RUN_ID}/planner.json", "w") as f:
# #         json.dump(plan, f, indent=2)

# #     # ----------- PHASE 2: DATA SUMMARY -----------
# #     data_summary = data_agent.summarize(plan)
# #     with open(f"logs/{RUN_ID}/data_summary.json", "w") as f:
# #         json.dump(data_summary, f, indent=2)

# #     # ----------- PHASE 3: INSIGHTS / HYPOTHESES -----------
# #     hypotheses = insight_agent.generate(plan, data_summary)
# #     with open(f"logs/{RUN_ID}/hypotheses.json", "w") as f:
# #         json.dump(hypotheses, f, indent=2)

# #     # ----------- PHASE 4: EVALUATION -----------
# #     validated = evaluator.validate(plan, hypotheses, data_summary)
# #     with open(f"reports/insights.json", "w") as f:
# #         json.dump(validated, f, indent=2)

# #     # ----------- PHASE 5: CREATIVE IMPROVEMENTS -----------
# #     creatives = creative_agent.generate(plan, data_summary, validated)
# #     with open(f"reports/creatives.json", "w") as f:
# #         json.dump(creatives, f, indent=2)

# #     # ----------- PHASE 6: FINAL REPORT -----------
# #     report_text = evaluator.generate_report(query, data_summary, validated, creatives)
# #     with open(report_path, "w", encoding="utf-8") as f:
# #         f.write(report_text)

# #     print("\n🎉 Run complete.")
# #     print("Generated:")
# #     print("- reports/insights.json")
# #     print("- reports/creatives.json")
# #     print("- reports/report.md")
# #     print(f"- logs stored in logs/{RUN_ID}")

# def main(query: str):

#     RUN_ID = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

#     ensure_dirs("reports")
#     ensure_dirs("logs")
#     ensure_dirs(f"logs/{RUN_ID}")

#     planner = PlannerAgent()
#     data_agent = DataAgent()
#     insight_agent = InsightAgent()
#     evaluator = EvaluatorAgent()
#     creative_agent = CreativeAgent()

#     # ----------- PHASE 1: PLANNING -----------
#     # plan = planner.create_plan(query)
#     # with open(f"logs/{RUN_ID}/planner.json", "w", encoding="utf-8") as f:
#     #     json.dump(plan, f, indent=2, ensure_ascii=False)

#     def convert(o):
#         if isinstance(o, (pd.Timestamp,)):
#             return str(o)
#         return o

#     with open(os.path.join(log_dir, "data_summary.json"), "w", encoding="utf-8") as f:
#         json.dump(data_summary, f, indent=2, ensure_ascii=False, default=convert)


    

# def convert(o):
#     if isinstance(o, (pd.Timestamp,)):
#         return str(o)
#     return o

# with open(os.path.join(log_dir, "data_summary.json"), "w", encoding="utf-8") as f:
#     json.dump(data_summary, f, indent=2, ensure_ascii=False, default=convert)


#     # ----------- PHASE 2: DATA SUMMARY -----------
#     data_summary = data_agent.summarize(plan)
#     with open(f"logs/{RUN_ID}/data_summary.json", "w", encoding="utf-8") as f:
#         json.dump(data_summary, f, indent=2, ensure_ascii=False)

#     # ----------- PHASE 3: INSIGHTS -----------
#     hypotheses = insight_agent.generate(plan, data_summary)
#     with open(f"logs/{RUN_ID}/hypotheses.json", "w", encoding="utf-8") as f:
#         json.dump(hypotheses, f, indent=2, ensure_ascii=False)

#     # ----------- PHASE 4: EVALUATION -----------
#     validated = evaluator.validate(plan, hypotheses, data_summary)
#     with open("reports/insights.json", "w", encoding="utf-8") as f:
#         json.dump(validated, f, indent=2, ensure_ascii=False)

#     # ----------- PHASE 5: CREATIVE IDEAS -----------
#     creatives = creative_agent.generate(plan, data_summary, validated)
#     with open("reports/creatives.json", "w", encoding="utf-8") as f:
#         json.dump(creatives, f, indent=2, ensure_ascii=False)

#     # ----------- PHASE 6: FINAL REPORT -----------
#     report_text = evaluator.generate_report(query, data_summary, validated, creatives)

#     report_path = "reports/report.md"
#     with open(report_path, "w", encoding="utf-8") as f:
#         f.write(report_text)

#     print("\n🎉 Run complete.")
#     print("Generated:")
#     print("- reports/insights.json")
#     print("- reports/creatives.json")
#     print("- reports/report.md")
#     print(f"- logs stored in logs/{RUN_ID}")



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("query", help="Example: 'Analyze ROAS drop'")
#     args = parser.parse_args()
#     main(args.query)







import argparse
import json
import os
import datetime
import pandas as pd

from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.evaluator import EvaluatorAgent
from agents.creative_agent import CreativeAgent


def ensure_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Helper for JSON serialization
def json_friendly(o):
    if isinstance(o, pd.Timestamp):
        return o.isoformat()
    return str(o)


def main(query: str):

    # Unique run folder
    RUN_ID = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_dir = f"logs/{RUN_ID}"

    # Create folders
    ensure_dirs("reports")
    ensure_dirs("logs")
    ensure_dirs(log_dir)

    # Create agents
    planner = PlannerAgent()
    data_agent = DataAgent()
    insight_agent = InsightAgent()
    evaluator = EvaluatorAgent()
    creative_agent = CreativeAgent()

    # ----------- PHASE 1: PLANNING -----------
    plan = planner.create_plan(query)
    with open(os.path.join(log_dir, "planner.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    # ----------- PHASE 2: DATA SUMMARY -----------
    data_summary = data_agent.summarize(plan)
    with open(os.path.join(log_dir, "data_summary.json"), "w", encoding="utf-8") as f:
        json.dump(data_summary, f, indent=2, ensure_ascii=False, default=json_friendly)

    # ----------- PHASE 3: INSIGHTS / HYPOTHESES -----------
    hypotheses = insight_agent.generate(plan, data_summary)
    with open(os.path.join(log_dir, "hypotheses.json"), "w", encoding="utf-8") as f:
        json.dump(hypotheses, f, indent=2, ensure_ascii=False)

    # ----------- PHASE 4: EVALUATION -----------
    validated = evaluator.validate(plan, hypotheses, data_summary)
    with open("reports/insights.json", "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2, ensure_ascii=False)

    # ----------- PHASE 5: CREATIVE IDEAS -----------
    creatives = creative_agent.generate(plan, data_summary, validated)
    with open("reports/creatives.json", "w", encoding="utf-8") as f:
        json.dump(creatives, f, indent=2, ensure_ascii=False)

    # ----------- PHASE 6: FINAL REPORT -----------
    report_text = evaluator.generate_report(query, data_summary, validated, creatives)

    report_path = "reports/report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    # ----------- DONE -----------
    print("\n🎉 Run complete.")
    print("Generated:")
    print("- reports/insights.json")
    print("- reports/creatives.json")
    print("- reports/report.md")
    print(f"- logs stored in {log_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Example: 'Analyze ROAS drop'")
    args = parser.parse_args()
    main(args.query)
