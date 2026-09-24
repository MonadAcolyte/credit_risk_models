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

2026-09-23: `~/src/credit_risk/data.py`; RENAMES; Target renamed to `default`, PAY_0 to PAY_1
The source spreadsheet's target name contains spaces and is awkward to use in code. PAY_0 is renamed so the repayment status columns run PAY_1 to PAY_6, matching BILL_AMT1–6 and PAY_AMT1–6 (all indexed from September 2005 back to April 2005). The spreadsheet's first header row (X1…X23, Y) is skipped by reading with header=1.

2026-09-24: `~/src/credit_risk/data.py`; clean; Undocumented category codes merged into "other"
EDUCATION 0, 5 and 6 (445 rows) are not in the dataset documentation and are merged into 4 ("others"); MARRIAGE 0 (54 rows) is merged into 3 ("others"). The groups are too small to estimate reliably on their own, and a scorecard needs every category to carry a meaningful weight of evidence. PAY_* values -2 and 0 are kept as they are: they are common, and their default rates differ from the documented -1, so they carry information. Negative bill amounts and the 35 records that duplicate another apart from ID (mostly dormant accounts with no bills or payments) are kept as genuine customers. Raw data is never modified; clean() returns a copy.

2026-09-24: `~/src/credit_risk/data.py`; make_split / load_splits; Frozen 60/20/20 stratified split saved by ID
The split is stratified on the target so every part keeps the 22.1% default rate. Only the ID-to-split assignment is saved; cleaning is cheap and deterministic, so the cleaned data is rebuilt from raw each time. make_split refuses to overwrite a saved split unless told to, and load_splits omits the test set unless include_test=True, so the test set cannot be used by accident before the final evaluation.

2026-09-24: `~/configs/uci_taiwan.toml`; assumptions.cost_ratio; Cost ratio of 5:1 assumed
A missed defaulter is assumed to cost five times a wrongly declined good customer: unsecured card losses given default are high (roughly 70–90% of the balance), while the revenue lost from a good customer is roughly 10–20% of the balance a year. With calibrated probabilities the cost-minimising cut-off is 1 / (1 + ratio), about 0.17. This is an assumption, and results will be tested for sensitivity to it.
