🚀 Kasparro Agentic Facebook Performance Analyst

A fully autonomous multi-agent system that analyzes Facebook Ads performance, explains ROAS/CTR fluctuations, and generates new high-performing creative ideas — all using a structured, explainable, agent-driven pipeline.

This project was built as part of the Kasparro Applied AI Engineer Assignment, following their guidelines for:

Agentic reasoning

Quantitative validation

Creative generation

Structured prompts

Clean architecture

Human-readable marketer reports




🧠 Why This Project Exists

Modern marketing teams struggle with:

❌ Unclear why ROAS dropped
❌ Too many campaigns to manually evaluate
❌ Creative fatigue not detected early
❌ No structured explanation or direction
❌ No system that both analyzes data and generates creative fixes

This project solves these by using a multi-agent AI system that thinks, analyzes, validates, and creates — all on its own.


# System Architecture

User Query  →  Planner Agent
                  │
                  ▼
            Data Agent
      (summaries, trends, CTR/ROAS)
                  │
                  ▼
           Insight Agent
      (hypothesis generation)
                  │
                  ▼
          Evaluator Agent
 (quantitative validation + evidence)
                  │
                  ▼
    Creative Improvement Agent
 (new creatives + CTAs + A/B plan)
                  │
                  ▼
            Final Report


Each agent has one job, making the system easy to reason about, debug, and extend.

# Features
✓ Multi-Agent Reasoning

Each agent performs a specific responsibility.
This keeps reasoning clean and transparent.


✓ Data-Driven Ad Diagnosis

The system identifies:

CTR drops

ROAS fluctuations

Creative fatigue

Audience mismatch

Spend anomalies

✓ Quantitative Hypothesis Validation

Not just “I think”, but backed by numbers:

Before/after CTR

% change

ROAS shifts

Confidence scoring

✓ Creative Recommendations

The system generates 5 new creative ideas for each low-performing campaign:

emotional angles

urgency hooks

value propositions

problem–solution framing

strong CTAs

A/B test-ready variants

✓ Human-Friendly Marketing Report

A final, clean report.md suitable for marketers and executives.


# Project Structure

Agentic_Facebook_Performance_Analyst/
│
├─ src/
│   ├─ run.py
│   └─ agents/
│       ├─ planner.py
│       ├─ data_agent.py
│       ├─ insight_agent.py
│       ├─ evaluator.py
│       └─ creative_agent.py
│
├─ prompts/
│   ├─ planner_prompt.md
│   ├─ data_prompt.md
│   ├─ insight_prompt.md
│   ├─ evaluator_prompt.md
│   └─ creative_prompt.md
│
├─ reports/
│   ├─ insights.json          
│   ├─ creatives.json         
│   └─ report.md              
│
├─ logs/
│
├─ config/
│   └─ config.yaml
│
├─ data/
│   └─ synthetic_fb_ads_undergarments.csv
│
├─ agent_graph.md
├─ design_rationale.md
└─ README.md



# How to Run

### **1. Place dataset here:**
   data/synthetic_fb_ads_undergarments.csv

### **2. Run from pipeline:**
   python src/run.py "Analyze ROAS drop"



### **3. Outputs will be generated in:**

reports/
 insights.json
 creatives.json
 report.md

logs/<run_id>/


# Sample Output
  samples/sample_output_run.txt



You’ll see:
   agent-by-agent flow
   insights discovered
   creatives generated
   logs created
   full report generated


# Agents (Human Explanation)
 # Planner Agent

“Hmm… what does the user want? What steps should we follow?”

Creates a clear plan with:

time windows

thresholds

task flow

# Data Agent

“Let me open the dataset and compute everything.”

loads CSV

CTR & ROAS calculation

recent vs prior windows

identifies low CTR campaigns

# Insight Agent

“Based on the data… here’s what might have happened.”

Creates hypotheses:

creative drop

fatigue

audience mismatch

spend shift

Follows Think → Analyze → Conclude reasoning.

# Evaluator Agent

“Let's check whether the hypothesis is actually true.”

Runs quantitative checks:

before vs after CTR

% change

confidence score

verdict: supported / not supported / inconclusive

# Creative Agent

“Campaign ka CTR low hai? Let’s fix it!”

Generates:

emotional creatives

urgency hooks

value-driven lines

CTAs

A/B plan

These are tailored to undergarment niche marketing.

# Outputs Explained
   insights.json

Structured, evidence-based hypotheses with confidence.

   creatives.json

New creative ideas + A/B testing plan.

 report.md

A clear, simple, marketing-friendly summary.

# Tech Stack

Python

Pandas

Numpy

Agent-based architecture

Structured prompting

Clean JSON outputs

Lightweight, extendable, and production-friendly.

## Why This Submission Stands Out

   This project demonstrates:

      Clean system design
      Multi-agent thinking
      Real data analysis
      Quantitative hypothesis validation
      Marketing creative understanding
      Strong documentation
      Clean, readable code
      Logs + reproducibility

## Exactly what companies look for in an Applied AI Engineer.

  # Author

    Sunny Anand
    AI Engineer | ML | Agentic Systems | Data Analyst