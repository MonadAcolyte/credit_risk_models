# credit_risk_models

# tree (planned)

credit_risk_models/
├── CLAUDE.md, ARCH_DECISIONS.md, README.md, LICENSE, .gitignore
├── MODEL_CARD.md
├── pyproject.toml # dependencies (runtime + dev group), ruff and pytest config
├── requirements.txt # pinned pip freeze export
├── configs/
│   └── uci_taiwan.toml # paths, seed, split ratios, cut-off, cost ratio
├── data/
│   ├── README.md # source, citation, licence
│   ├── raw/ # gitignored
│   └── processed/ # gitignored (cleaned data + frozen split indices)
├── scripts/
│   └── download_data.py
├── src/credit_risk/ # logic here, called by notebooks
│   ├── __init__.py
│   ├── config.py # loads configs/*.toml
│   ├── data.py # load, clean (EDUCATION / PAY_* codes), split
│   ├── scorecard.py # optbinning WoE/IV, logistic regression, points
│   ├── challenger.py # LightGBM + tuning
│   ├── calibration.py # Platt / isotonic wrappers
│   ├── metrics.py # AUC, Gini, KS, Brier, log loss, bootstrap CIs
│   ├── fairness.py # group default rates, approval rates, calibration
│   ├── stability.py # PSI
│   └── plots.py # reliability diagrams etc., consistent style
├── notebooks/ # numbered, narrative, outputs stripped
│   ├── 01_framing_eda.ipynb
│   ├── 02_scorecard.ipynb
│   ├── 03_challenger.ipynb
│   ├── 04_calibration.ipynb
│   ├── 05_explainability.ipynb
│   ├── 06_fairness_stability.ipynb
│   └── 07_final_test_evaluation.ipynb # only notebook to touch the test set
├── tests/ # pytest
│   ├── test_metrics.py
│   └── test_stability.py
├── reports/
│   ├── figures/ # saved plots
│   └── tables/ # saved result tables
├── models/ # gitignored fitted artefacts
└── drafts/ # gitignored

