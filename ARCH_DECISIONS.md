# Architectural and Design decisions

2026-09-23: `~/`; repository layout; Logic in src/, narrative in notebooks/
All reusable and testable logic lives in the `credit_risk` package under src/. Notebooks are numbered, import from the package and only narrate results, so every number can be traced to tested code. The package is a flat set of modules to keep it easy to explain; further models or datasets get their own config and loader.

2026-09-23: `~/pyproject.toml`; environment; Plain venv with everything in TOML
Dependencies sit in pyproject.toml (runtime under [project], tooling under [dependency-groups] dev) and configs in configs/*.toml, read with the standard library's tomllib. This avoids extra tools and PyYAML's implicit type coercion, and anyone can reproduce the environment with pip alone. requirements.txt is produced by `pip freeze` as the pinned record.

2026-09-23: `~/notebooks/`; notebook outputs; Notebooks committed stripped
Notebook outputs are stripped with nbstripout to keep diffs clean. Any output worth keeping (figures, tables) is saved individually to reports/.

2026-09-23: `~/src/credit_risk/challenger.py`; challenger model; LightGBM as the challenger
LightGBM is fast on tabular data and has native SHAP support through TreeExplainer, which the explainability step relies on.

2026-09-23: `~/notebooks/07_final_test_evaluation.ipynb`; test set; Test set touched only in the final notebook
The split is made once with a fixed seed and the indices are saved. Only the final notebook evaluates on the test set, so it stays an unbiased estimate.
