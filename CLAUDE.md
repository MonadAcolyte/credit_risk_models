# Context file for this repository

# REPO RULES (Don't edit this title or its contents, keep it in line 3)

Important rules for the coding agent:
    - Everything is to be written in English GB (Save local terms)
    - Don't edit the root level README
    - When commenting the code don't include the reasoning for things, instead make a note in the `ARCH_DECISIONS.md` with the format below:

    YYYY-MM-DD: `~/path/to/file`; name_of_thing; Title
    Reasoning goes here

You may also include key decisions in this context file if needed.

If you wish to edit anything barred by these rules, suggest it over the chat or leave a draft in drafts/

# ...
    

# Project conventions

- Aim: portfolio project; a WoE scorecard (champion) against a LightGBM challenger on the UCI Taiwan credit card default data, with calibration as the core and a MODEL_CARD.md following PRA SS1/23. The brief is in drafts/project_finance.txt. More models will follow once this one is done.
- Environment: plain venv in `venv/` (Python 3.13). Dependencies in `pyproject.toml` (runtime + `dev` group) and pinned in `requirements.txt` (pip freeze, with `-e .` added by hand at the end). Configs in `configs/*.toml`, read by `credit_risk.config.load_config()`, which resolves `[paths]` against the repo root.
- Logic lives in `src/credit_risk/`; notebooks are numbered, import from the package, and narrate. Notebooks start with `%load_ext autoreload` / `%autoreload 2`.
- Notebook outputs are stripped by the nbstripout git filter; figures worth keeping are saved to `reports/figures/` with the notebook's number as prefix (e.g. `01_...png`).
- Data: `scripts/download_data.py` fetches and SHA-256-verifies the raw file. `data.load_raw()` → `data.clean()` → `data.load_splits()`. The 60/20/20 stratified split (seed 2112) is frozen in `data/processed/split.parquet`; never regenerate it. The test set is only loaded (`include_test=True`) in notebook 07.
- Exploratory analysis and all fitting use the training set only; tuning uses validation.
- The user writes the notebooks; the agent proposes cells in chat for them to paste unless asked otherwise. Plots use matplotlib with the ggplot style.
- Run `ruff check` / `ruff format` on `src/` and `scripts/` after edits.
