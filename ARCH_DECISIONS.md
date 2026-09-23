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

2026-09-23: `~/scripts/download_data.py`; main; Download verified by SHA-256
The extracted .xls is checked against a SHA-256 stored in the config, both on download and when the file already exists, so every run is known to use the same bytes. UCI has changed file formats and URLs before. The file is renamed to uci_taiwan_default.xls to remove spaces from the path. Only the standard library is used, so the data can be fetched before any dependencies are installed.

2026-09-23: `~/src/credit_risk/config.py`; load_config; Paths resolved against the project root
Paths in [paths] are converted to absolute paths from the repository root, so scripts, notebooks and tests find the same files whatever the working directory. This relies on the package being installed in editable mode (`pip install -e .`).

2026-09-23: `~/requirements.txt`; environment; HiGHS import warning from CVXPY accepted
When optbinning is imported, OR-Tools loads its bundled HiGHS library before CVXPY loads highspy, so highspy's extension fails with an undefined symbol and CVXPY logs an ImportError for the HiGHS solver. Imports still succeed. The scorecard's binning uses OR-Tools, and CVXPY is only reached through ropwr for piecewise binning, which this project does not use. Revisit if piecewise binning is ever needed.
