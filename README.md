# credit_risk_models

# tree (planned)

credit_risk_models/
├── CLAUDE.md, ARCH_DECISIONS.md, README.md, LICENCE
├── MODEL_CARD.md
├── pyproject.toml # dependencies + ruff + pytest config
├── requirements.txt # pinned export, as the brief asks
├── configs/
│   └── uci_taiwan.yaml # paths, seed, split ratios, cut-off, cost ratio
├── data/
│   ├── README.md # source, citation, licence
│   ├── raw/ # gitignored
│   └── processed/ # gitignored (cleaned data + frozen split indices)
├── scripts/
│   └── download_data.py
├── src/credit_risk/ # logic here, called by notebooks
│   ├── config.py
│   ├── data.py # load, clean (EDUCATION / PAY_* codes), split
│   ├── scorecard.py # optbinning WoE/IV, logistic regression, points
│   ├── challenger.py # LightGBM + tuning
│   ├── calibration.py # Platt / isotonic wrappers
│   ├── metrics.py # AUC, Gini, KS, Brier, log loss, bootstrap CIs
│   ├── fairness.py
│   ├── stability.py # PSI
│   └── plots.py # reliability diagrams etc., consistent style
├── notebooks/ # numbered, narrative
│   ├── 01_framing_eda.ipynb
│   ├── 02_scorecard.ipynb
│   ├── 03_challenger.ipynb
│   ├── 04_calibration.ipynb
│   ├── 05_explainability.ipynb
│   ├── 06_fairness_stability.ipynb
│   └── 07_final_test_evaluation.ipynb
├── tests/ # pytest, focused on metrics.py / stability.py
├── reports/figures/, reports/tables/
├── models/ # gitignored fitted artefacts
└── drafts/ # already gitignored
