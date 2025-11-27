## Kasparro — Agentic Facebook Performance Analyst
 # Applied AI Engineer Assignment — by Sunny Anand

##  Demo Video  
  # Watch the full demo video here: [Click to Watch](https://drive.google.com/file/d/1vyIdfw2YAV3kk6LmH_-_vaPwa4T0-4-Q/view?usp=sharing)



# Overview

This project implements a multi-agent autonomous analytics system that diagnoses Facebook Ads ROAS fluctuations, identifies drivers behind performance changes, and generates data-grounded creative recommendations.

The architecture follows Kasparro’s required 5-agent pipeline:
 1. Planner Agent → Breaks user query into tasks
 2. Data Agent → Reads + summarizes dataset
 3. Insight Agent → Generates hypotheses
 4. Evaluator Agent → Quantitatively validates hypotheses
 5. Creative Agent → Creates new CTR-optimized creative variations

Output Files are Automatically saved into the /report folder.


## Repository Structure.
    
kasparro-agentic-fb-analyst-sunny-anand/
│
├── README.md
├── requirements.txt
├── config/
│   └── config.yaml
│
├── data/
│   ├── sample_fb_ads.csv
│   └── README.md
│
├── src/
│   ├── run.py
│   ├── agents/
│   │   ├── planner.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator.py
│   │   └── creative_agent.py
│   └── utils/
│       └── text_cleaning.py
│
├── prompts/
│   ├── planner_prompt.md
│   ├── insight_prompt.md
│   ├── evaluator_prompt.md
│   └── creative_prompt.md
│
├── reports/
│   ├── report.md
│   ├── insights.json
│   └── creatives.json
│
├── logs/
│   └── (Auto-generated run logs)
│
├── tests/
│   └── test_evaluator.py
│
└── agent_graph.md


# Setup
  1. Create a virtual env
      python -m venv venv
      source venv/bin/activate      # Windows: venv\Scripts\activate

  2. Install dependencies
      pip install -r requirements.txt
  
  3. Configure data path
    Edit config/config.yaml:

    data_path: "data/sample_fb_ads.csv"
    confidence_min: 0.6
    random_seed: 42
    use_sample_data: true


    If using full dataset:
       data_path: "data/synthetic_fb_ads_undergarments.csv"
       use_sample_data: false


## How To Run 
   --python src/run.py "Analyze ROAS drop"
                     or
   --python src/run.py "Bhai mera ROAS gir gaya help!"


# Output Generated:
   * reports/report.md → human-ready marketing summary

   * reports/insights.json → validated hypotheses

   * reports/creatives.json → CTR-optimized creative ideas

   * logs/<RUN_ID>/ → structured logs for evaluation


## Architecture Diagram: 
   
   # AGENT FLOW: -----

        User Query
            ↓
        Planner Agent
            ↓ plan.json
        Data Agent ← raw CSV
            ↓ data_summary.json
        Insight Agent
            ↓ hypotheses.json
        Evaluator Agent
            ↓ insights.json (validated)
        Creative Agent
            ↓ creatives.json
        Final Report Generator
            ↓ report.md


## Validation Logic (Evaluator Agent)
     
Hypothesis confidence is based on:

| Metric             |        Meaning                     |
| ------------------ | ---------------------------------- |
| **CTR Shift**      | Prior vs recent 7-day CTR change   |
| **Impressions**    | Ensures statistical significance   |
| **ROAS Direction** | Whether leads align with ROAS drop |



Supported Hypothesis Conditions

   * CTR drop ≥ 25%

   * Recent impressions ≥ 5000

   * Boost confidence if ROAS also dropped




## Creative Generation Logic (Creative Agent)
Each low-CTR campaign gets:
 * Top keywords extracted from existing creative_message
 * 5 new creative variants
    * Emotional
    * Urgency
    * Value-focused
    * Problem→Solution
    * Social proof

 * Automatic A/B test plan:
    "metric": "CTR", "duration_days": 7


## Example Run Output

    Men ComfortMax Lau Ch — supported
    CTR dropped by -55.6%
    Impressions: 120,918
    Reason: Audience fatigue + creative decay
    Recommendation: Refresh creative with new "soft", "confidence", "vests" messaging


## Testing
  One test is included:
    tests/test_evaluator.py

  Run tests:
    pytest tests/


## Observability 
   
   All runs automatically store:
     logs/<RUN_ID>/planner.json
     logs/<RUN_ID>/data_summary.json
     logs/<RUN_ID>/hypotheses.json

   These logs make the agent pipeline evaluatable & debuggable.

## Release(v1.0)
   Commit Hash: 92ac8e5


   File                                                  Link
 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Final Report(reports.md)                                 https://github.com/ANANDSUNNY0899/kasparro-agentic-fb-analyst-sunny-anand/blob/main/reports/report.md

Validated Insights(insights.json)                        https://github.com/ANANDSUNNY0899/kasparro-agentic-fb-analyst-sunny-anand/blob/main/reports/insights.json

Creative Recommendations (creatives.json)                https://github.com/ANANDSUNNY0899/kasparro-agentic-fb-analyst-sunny-anand/blob/main/reports/creatives.json


## Command Used For Generation

    python src/run.py "Analyze ROAS drop"
            
            

## Self-Review PR
    Create PR with titles:
      “Self Review — Kasparro Agentic FB Analyst Assignment”








       



